# shellcheck disable=SC2148
# shellcheck disable=SC2155
# clash-cli.sh - Main control script for clash-cli

_set_system_proxy() {
    local auth=$(sudo "$BIN_YQ" '.authentication[0] // ""' "$CLASH_CONFIG_RUNTIME")
    [ -n "$auth" ] && auth=$auth@

    local http_proxy_addr="http://${auth}127.0.0.1:${MIXED_PORT}"
    local socks_proxy_addr="socks5h://${auth}127.0.0.1:${MIXED_PORT}"
    local no_proxy_addr="localhost,127.0.0.1,::1"

    export http_proxy=$http_proxy_addr
    export https_proxy=$http_proxy
    export HTTP_PROXY=$http_proxy
    export HTTPS_PROXY=$http_proxy

    export all_proxy=$socks_proxy_addr
    export ALL_PROXY=$all_proxy

    export no_proxy=$no_proxy_addr
    export NO_PROXY=$no_proxy

    sudo "$BIN_YQ" -i '.system-proxy.enable = true' "$CLASH_CONFIG_MIXIN"
}

_unset_system_proxy() {
    unset http_proxy
    unset https_proxy
    unset HTTP_PROXY
    unset HTTPS_PROXY
    unset all_proxy
    unset ALL_PROXY
    unset no_proxy
    unset NO_PROXY

    sudo "$BIN_YQ" -i '.system-proxy.enable = false' "$CLASH_CONFIG_MIXIN"
}

_clash_on() {
    _get_proxy_port
    systemctl is-active "$BIN_KERNEL_NAME" >&/dev/null || {
        sudo systemctl start "$BIN_KERNEL_NAME" >/dev/null || {
            _failcat '启动失败: 执行 clash-cli status 查看日志'
            return 1
        }
    }
    _set_system_proxy
    _okcat "$(_msg 'proxy_on')"
}

watch_proxy() {
    # 新开交互式shell，且无代理变量时
    [ -z "$http_proxy" ] && [[ $- == *i* ]] && {
        # root用户自动开启代理环境（普通用户会触发sudo验证密码导致卡住）
        _is_root && _clash_on
    }
}

_clash_off() {
    sudo systemctl stop "$BIN_KERNEL_NAME" && _okcat "$(_msg 'proxy_off')" ||
        _failcat '关闭失败: 执行 "clash-cli status" 查看日志' || return 1
    _unset_system_proxy
}

_clash_restart() {
    { _clash_off && _clash_on; } >&/dev/null
}

_clash_proxy() {
    case "$1" in
    on)
        systemctl is-active "$BIN_KERNEL_NAME" >&/dev/null || {
            _failcat '代理程序未运行，请执行 clash-cli on 开启代理环境'
            return 1
        }
        _set_system_proxy
        _okcat "$(_msg 'proxy_enabled')"
        ;;
    off)
        _unset_system_proxy
        _okcat "$(_msg 'proxy_disabled')"
        ;;
    status)
        local system_proxy_status=$(sudo "$BIN_YQ" '.system-proxy.enable' "$CLASH_CONFIG_MIXIN" 2>/dev/null)
        [ "$system_proxy_status" = "false" ] && {
            _failcat "系统代理：关闭"
            return 1
        }
        _okcat "系统代理：开启
http_proxy： $http_proxy
socks_proxy：$all_proxy"
        ;;
    *)
        cat <<EOF
用法: clash-cli proxy [on|off|status]
    on      开启系统代理
    off     关闭系统代理
    status  查看系统代理状态
EOF
        ;;
    esac
}

_clash_status() {
    sudo systemctl status "$BIN_KERNEL_NAME" "$@"
}

_clash_ui() {
    _get_ui_port
    # 公网ip
    # ifconfig.me
    local query_url='api64.ipify.org'
    local public_ip=$(curl -s --noproxy "*" --connect-timeout 2 $query_url)
    local public_address="http://${public_ip:-公网}:${UI_PORT}/ui"
    # 内网ip
    # ip route get 1.1.1.1 | grep -oP 'src \K\S+'
    local local_ip=$(hostname -I | awk '{print $1}')
    local local_address="http://${local_ip}:${UI_PORT}/ui"
    printf "\n"
    printf "╔═══════════════════════════════════════════════╗\n"
    printf "║                %s                  ║\n" "$(_okcat "$(_msg 'web_console')")"
    printf "║═══════════════════════════════════════════════║\n"
    printf "║                                               ║\n"
    printf "║     🔓 注意放行端口：%-5s                    ║\n" "$UI_PORT"
    printf "║     🏠 内网：%-31s  ║\n" "$local_address"
    printf "║     🌏 公网：%-31s  ║\n" "$public_address"
    printf "║     ☁️  公共：%-31s  ║\n" "$URL_CLASH_UI"
    printf "║                                               ║\n"
    printf "╚═══════════════════════════════════════════════╝\n"
    printf "\n"
}

_merge_config_restart() {
    local backup="/tmp/rt.backup"
    sudo cat "$CLASH_CONFIG_RUNTIME" 2>/dev/null | sudo tee $backup >&/dev/null
    sudo "$BIN_YQ" eval-all '. as $item ireduce ({}; . *+ $item) | (.. | select(tag == "!!seq")) |= unique' \
        "$CLASH_CONFIG_MIXIN" "$CLASH_CONFIG_RAW" "$CLASH_CONFIG_MIXIN" | sudo tee "$CLASH_CONFIG_RUNTIME" >&/dev/null
    _valid_config "$CLASH_CONFIG_RUNTIME" || {
        sudo cat $backup | sudo tee "$CLASH_CONFIG_RUNTIME" >&/dev/null
        _error_quit "验证失败：请检查 Mixin 配置"
    }
    _clash_restart
}

_clash_secret() {
    case "$#" in
    0)
        _okcat "$(_msg 'current_secret')$(sudo "$BIN_YQ" '.secret // ""' "$CLASH_CONFIG_RUNTIME")"
        ;;
    1)
        sudo "$BIN_YQ" -i ".secret = \"$1\"" "$CLASH_CONFIG_MIXIN" || {
            _failcat "密钥更新失败，请重新输入"
            return 1
        }
        _merge_config_restart
        _okcat "$(_msg 'secret_updated')"
        ;;
    *)
        _failcat "密钥不要包含空格或使用引号包围"
        ;;
    esac
}

_tunstatus() {
    local tun_status=$(sudo "$BIN_YQ" '.tun.enable' "${CLASH_CONFIG_RUNTIME}")
    # shellcheck disable=SC2015
    [ "$tun_status" = 'true' ] && _okcat "$(_msg 'tun_status_on')" || _failcat "$(_msg 'tun_status_off')"
}

_tunoff() {
    _tunstatus >/dev/null || return 0
    sudo "$BIN_YQ" -i '.tun.enable = false' "$CLASH_CONFIG_MIXIN"
    _merge_config_restart && _okcat "$(_msg 'tun_disabled')"
}

_tunon() {
    _tunstatus 2>/dev/null && return 0
    sudo "$BIN_YQ" -i '.tun.enable = true' "$CLASH_CONFIG_MIXIN"
    _merge_config_restart
    sleep 0.5s
    sudo journalctl -u "$BIN_KERNEL_NAME" --since "1 min ago" | grep -E -m1 'unsupported kernel version|Start TUN listening error' && {
        _tunoff >&/dev/null
        _error_quit '不支持的内核版本'
    }
    _okcat "$(_msg 'tun_enabled')"
}

_clash_tun() {
    case "$1" in
    on)
        _tunon
        ;;
    off)
        _tunoff
        ;;
    *)
        _tunstatus
        ;;
    esac
}

_clash_update() {
    local url=$(cat "$CLASH_CONFIG_URL")
    local is_auto

    case "$1" in
    auto)
        is_auto=true
        [ -n "$2" ] && url=$2
        ;;
    log)
        sudo tail "${CLASH_UPDATE_LOG}" 2>/dev/null || _failcat "暂无更新日志"
        return 0
        ;;
    *)
        [ -n "$1" ] && url=$1
        ;;
    esac

    # 如果没有提供有效的订阅链接（url为空或者不是http开头），则使用默认配置文件
    [ "${url:0:4}" != "http" ] && {
        _failcat "没有提供有效的订阅链接：使用 ${CLASH_CONFIG_RAW} 进行更新..."
        url="file://$CLASH_CONFIG_RAW"
    }

    # 如果是自动更新模式，则设置定时任务
    [ "$is_auto" = true ] && {
        sudo grep -qs 'clash-cli update' "$CLASH_CRON_TAB" || echo "0 0 */2 * * $_SHELL -i -c 'clash-cli update $url'" | sudo tee -a "$CLASH_CRON_TAB" >&/dev/null
        _okcat "$(_msg 'auto_update_set')" && return 0
    }

    _okcat '👌' "$(_msg 'update_downloading')"
    sudo cat "$CLASH_CONFIG_RAW" | sudo tee "$CLASH_CONFIG_RAW_BAK" >&/dev/null

    _rollback() {
        _failcat '🍂' "$1"
        sudo cat "$CLASH_CONFIG_RAW_BAK" | sudo tee "$CLASH_CONFIG_RAW" >&/dev/null
        _failcat '❌' "[$(date +"%Y-%m-%d %H:%M:%S")] 订阅更新失败：$url" 2>&1 | sudo tee -a "${CLASH_UPDATE_LOG}" >&/dev/null
        _error_quit
    }

    _download_config "$CLASH_CONFIG_RAW" "$url" || _rollback "下载失败：已回滚配置"
    _valid_config "$CLASH_CONFIG_RAW" || _rollback "转换失败：已回滚配置，转换日志：$BIN_SUBCONVERTER_LOG"

    _merge_config_restart && _okcat '🍃' "$(_msg 'update_success')"
    echo "$url" | sudo tee "$CLASH_CONFIG_URL" >&/dev/null
    _okcat '✅' "[$(date +"%Y-%m-%d %H:%M:%S")] 订阅更新成功：$url" | sudo tee -a "${CLASH_UPDATE_LOG}" >&/dev/null
}

_clash_mixin() {
    case "$1" in
    -e)
        sudo vim "$CLASH_CONFIG_MIXIN" && {
            _merge_config_restart && _okcat "$(_msg 'config_updated')"
        }
        ;;
    -r)
        less -f "$CLASH_CONFIG_RUNTIME"
        ;;
    *)
        less -f "$CLASH_CONFIG_MIXIN"
        ;;
    esac
}

function clash-cli() {
    case "$1" in
    on)
        _clash_on
        ;;
    off)
        _clash_off
        ;;
    ui)
        _clash_ui
        ;;
    status)
        shift
        _clash_status "$@"
        ;;
    proxy)
        shift
        _clash_proxy "$@"
        ;;
    tun)
        shift
        _clash_tun "$@"
        ;;
    mixin)
        shift
        _clash_mixin "$@"
        ;;
    secret)
        shift
        _clash_secret "$@"
        ;;
    update)
        shift
        _clash_update "$@"
        ;;
    lang)
        _clash_lang "$@"
        ;;
    *)
        _show_help
        ;;
    esac
}

# 语言切换功能
_clash_lang() {
    local lang="$2"

    case "$lang" in
        "zh"|"en")
            if set_language "$lang"; then
                _msg "lang_switched"
            else
                echo "Error: Failed to set language"
            fi
            ;;
        "")
            _msg "current_lang"
            ;;
        *)
            _msg "lang_usage"
            ;;
    esac
}

# 显示帮助信息
_show_help() {
    local current_lang=$(get_current_lang)

    if [[ "$current_lang" == "en" ]]; then
        cat <<EOF

Usage:
    clash-cli COMMAND [OPTION]

Commands:
    on                      Enable proxy
    off                     Disable proxy
    proxy    [on|off]       System proxy
    ui                      Panel address
    status                  Kernel status
    tun      [on|off]       Tun mode
    mixin    [-e|-r]        Mixin configuration
    secret   [SECRET]       Web secret
    update   [auto|log]     Update subscription
    lang     [zh|en]        Switch language

EOF
    else
        cat <<EOF

Usage:
    clash-cli COMMAND [OPTION]

Commands:
    on                      开启代理
    off                     关闭代理
    proxy    [on|off]       系统代理
    ui                      面板地址
    status                  内核状况
    tun      [on|off]       Tun 模式
    mixin    [-e|-r]        Mixin 配置
    secret   [SECRET]       Web 密钥
    update   [auto|log]     更新订阅
    lang     [zh|en]        切换语言

EOF
    fi
}
