# shellcheck disable=SC2148
# shellcheck disable=SC2034
# shellcheck disable=SC2155
[ -n "$BASH_VERSION" ] && set +o noglob
[ -n "$ZSH_VERSION" ] && setopt glob no_nomatch

# ==================== 多语言支持 ====================
CLASH_LANG_CONF="${CLASH_BASE_DIR}/lang.conf"

# 多语言消息字典
declare -A MSG_ZH MSG_EN

# 中文消息
MSG_ZH["proxy_on"]="😼 已开启代理环境"
MSG_ZH["proxy_off"]="😼 已关闭代理环境"
MSG_ZH["proxy_enabled"]="😼 系统代理：开启"
MSG_ZH["proxy_disabled"]="😼 系统代理：关闭"
MSG_ZH["tun_enabled"]="😼 Tun 模式已开启"
MSG_ZH["tun_disabled"]="😼 Tun 模式已关闭"
MSG_ZH["tun_status_on"]="😼 Tun 状态：开启"
MSG_ZH["tun_status_off"]="😾 Tun 状态：关闭"
MSG_ZH["secret_updated"]="😼 密钥更新成功，已重启生效"
MSG_ZH["current_secret"]="😼 当前密钥："
MSG_ZH["update_success"]="🍃 订阅更新成功"
MSG_ZH["update_downloading"]="👌 正在下载：原配置已备份..."
MSG_ZH["update_validating"]="🍃 下载成功：内核验证配置..."
MSG_ZH["auto_update_set"]="😼 已设置定时更新订阅"
MSG_ZH["mixin_view"]="😼 less 查看 mixin 配置"
MSG_ZH["mixin_edit"]="😼 vim 编辑 mixin 配置"
MSG_ZH["mixin_runtime"]="😼 less 查看 运行时 配置"
MSG_ZH["web_console"]="😼 Web 控制台"
MSG_ZH["note_open_port"]="🔓 注意放行端口：9090"
MSG_ZH["panel_address"]="🌍 面板地址：http://127.0.0.1:9090/ui"
MSG_ZH["uninstalled"]="✨ 已卸载，相关配置已清除"
MSG_ZH["enjoy"]="🎉 enjoy 🎉"
MSG_ZH["lang_switched"]="语言已切换为中文"
MSG_ZH["current_lang"]="当前语言：中文 (zh)"
MSG_ZH["lang_usage"]="用法: clash-cli lang [zh|en]"
MSG_ZH["config_updated"]="配置更新成功，已重启生效"

# 英文消息
MSG_EN["proxy_on"]="😼 Proxy environment enabled"
MSG_EN["proxy_off"]="😼 Proxy environment disabled"
MSG_EN["proxy_enabled"]="😼 System proxy: enabled"
MSG_EN["proxy_disabled"]="😼 System proxy: disabled"
MSG_EN["tun_enabled"]="😼 Tun mode enabled"
MSG_EN["tun_disabled"]="😼 Tun mode disabled"
MSG_EN["tun_status_on"]="😼 Tun status: enabled"
MSG_EN["tun_status_off"]="😾 Tun status: disabled"
MSG_EN["secret_updated"]="😼 Secret updated successfully, restarted"
MSG_EN["current_secret"]="😼 Current secret: "
MSG_EN["update_success"]="🍃 Subscription updated successfully"
MSG_EN["update_downloading"]="👌 Downloading: Original config backed up..."
MSG_EN["update_validating"]="🍃 Download successful: Kernel validating config..."
MSG_EN["auto_update_set"]="😼 Scheduled subscription update set"
MSG_EN["mixin_view"]="😼 less view mixin configuration"
MSG_EN["mixin_edit"]="😼 vim edit mixin configuration"
MSG_EN["mixin_runtime"]="😼 less view runtime configuration"
MSG_EN["web_console"]="😼 Web Console"
MSG_EN["note_open_port"]="🔓 Note: Open port: 9090"
MSG_EN["panel_address"]="🌍 Panel URL: http://127.0.0.1:9090/ui"
MSG_EN["uninstalled"]="✨ Uninstalled, related configurations cleared"
MSG_EN["enjoy"]="🎉 enjoy 🎉"
MSG_EN["lang_switched"]="Language switched to English"
MSG_EN["current_lang"]="Current language: English (en)"
MSG_EN["lang_usage"]="Usage: clash-cli lang [zh|en]"
MSG_EN["config_updated"]="Configuration updated successfully, restarted"

# 获取当前语言设置
get_current_lang() {
    if [[ -f "$CLASH_LANG_CONF" ]]; then
        source "$CLASH_LANG_CONF" 2>/dev/null
        echo "${LANG:-zh}"
    else
        echo "zh"
    fi
}

# 设置语言
set_language() {
    local lang="$1"
    if [[ "$lang" == "zh" || "$lang" == "en" ]]; then
        mkdir -p "$(dirname "$CLASH_LANG_CONF")"
        echo "LANG=$lang" > "$CLASH_LANG_CONF"
        return 0
    else
        return 1
    fi
}

# 翻译函数
_msg() {
    local key="$1"
    local current_lang=$(get_current_lang)

    if [[ "$current_lang" == "en" ]]; then
        echo "${MSG_EN[$key]:-$key}"
    else
        echo "${MSG_ZH[$key]:-$key}"
    fi
}
# ==================== 多语言支持结束 ====================

URL_GH_PROXY='https://gh-proxy.com/'
URL_CLASH_UI="http://board.zash.run.place"

SCRIPT_BASE_DIR='./script'
SCRIPT_FISH="${SCRIPT_BASE_DIR}/clash-cli.fish"

RESOURCES_BASE_DIR='./resources'
RESOURCES_BIN_DIR="${RESOURCES_BASE_DIR}/bin"
RESOURCES_CONFIG="${RESOURCES_BASE_DIR}/config.yaml"
RESOURCES_CONFIG_MIXIN="${RESOURCES_BASE_DIR}/mixin.yaml"

ZIP_BASE_DIR="${RESOURCES_BASE_DIR}/zip"
ZIP_CLASH=$(echo ${ZIP_BASE_DIR}/clash*)
ZIP_MIHOMO=$(echo ${ZIP_BASE_DIR}/mihomo*)
ZIP_YQ=$(echo ${ZIP_BASE_DIR}/yq*)
ZIP_SUBCONVERTER=$(echo ${ZIP_BASE_DIR}/subconverter*)
ZIP_UI="${ZIP_BASE_DIR}/yacd.tar.xz"

CLASH_BASE_DIR='/opt/clash'
CLASH_SCRIPT_DIR="${CLASH_BASE_DIR}/$(basename $SCRIPT_BASE_DIR)"
CLASH_CONFIG_URL="${CLASH_BASE_DIR}/url"
CLASH_CONFIG_RAW="${CLASH_BASE_DIR}/$(basename $RESOURCES_CONFIG)"
CLASH_CONFIG_RAW_BAK="${CLASH_CONFIG_RAW}.bak"
CLASH_CONFIG_MIXIN="${CLASH_BASE_DIR}/$(basename $RESOURCES_CONFIG_MIXIN)"
CLASH_CONFIG_RUNTIME="${CLASH_BASE_DIR}/runtime.yaml"
CLASH_UPDATE_LOG="${CLASH_BASE_DIR}/clash-cli-update.log"

_set_var() {
    local user=$USER
    local home=$HOME
    [ -n "$SUDO_USER" ] && {
        user=$SUDO_USER
        home=$(awk -F: -v user="$SUDO_USER" '$1==user{print $6}' /etc/passwd)
    }

    [ -n "$BASH_VERSION" ] && {
        _SHELL=bash
    }
    [ -n "$ZSH_VERSION" ] && {
        _SHELL=zsh
    }
    [ -n "$fish_version" ] && {
        _SHELL=fish
    }

    # rc配置文件
    command -v bash >&/dev/null && {
        SHELL_RC_BASH="${home}/.bashrc"
    }
    command -v zsh >&/dev/null && {
        SHELL_RC_ZSH="${home}/.zshrc"
    }
    command -v fish >&/dev/null && {
        SHELL_RC_FISH="${home}/.config/fish/conf.d/clash-cli.fish"
    }

    # 系统信息
    local os_info=$(cat /etc/os-release)
    echo "$os_info" | grep -iqsE "rhel|centos" && CLASH_CRON_TAB="/var/spool/cron/$user"
    echo "$os_info" | grep -iqsE "debian|ubuntu" && CLASH_CRON_TAB="/var/spool/cron/crontabs/$user"
}
_set_var

# shellcheck disable=SC2120
_set_bin() {
    local bin_base_dir="${CLASH_BASE_DIR}/bin"
    [ -n "$1" ] && bin_base_dir=$1
    BIN_CLASH="${bin_base_dir}/clash"
    BIN_MIHOMO="${bin_base_dir}/mihomo"
    BIN_YQ="${bin_base_dir}/yq"
    BIN_SUBCONVERTER_DIR="${bin_base_dir}/subconverter"
    BIN_SUBCONVERTER_CONFIG="$BIN_SUBCONVERTER_DIR/pref.yml"
    BIN_SUBCONVERTER_PORT="25500"
    BIN_SUBCONVERTER="${BIN_SUBCONVERTER_DIR}/subconverter"
    BIN_SUBCONVERTER_LOG="${BIN_SUBCONVERTER_DIR}/latest.log"

    [ -f "$BIN_CLASH" ] && {
        BIN_KERNEL=$BIN_CLASH
    }
    [ -f "$BIN_MIHOMO" ] && {
        BIN_KERNEL=$BIN_MIHOMO
    }
    BIN_KERNEL_NAME=$(basename "$BIN_KERNEL")
}
_set_bin

_set_rc() {
    [ "$1" = "unset" ] && {
        sed -i "\|$CLASH_SCRIPT_DIR|d" "$SHELL_RC_BASH" "$SHELL_RC_ZSH" 2>/dev/null
        rm -f "$SHELL_RC_FISH" 2>/dev/null
        return
    }

    echo "source $CLASH_SCRIPT_DIR/common.sh && source $CLASH_SCRIPT_DIR/clash-cli.sh && watch_proxy" |
        tee -a "$SHELL_RC_BASH" "$SHELL_RC_ZSH" >&/dev/null
    [ -n "$SHELL_RC_FISH" ] && /usr/bin/install $SCRIPT_FISH "$SHELL_RC_FISH"
}

# 获取内核文件mihomo优先
# 如果存在mihomo则优先使用clash作为备选
function _get_kernel() {
    [ -f "$ZIP_CLASH" ] && {
        ZIP_KERNEL=$ZIP_CLASH
        BIN_KERNEL=$BIN_CLASH
    }

    [ -f "$ZIP_MIHOMO" ] && {
        ZIP_KERNEL=$ZIP_MIHOMO
        BIN_KERNEL=$BIN_MIHOMO
    }

    [ ! -f "$ZIP_MIHOMO" ] && [ ! -f "$ZIP_CLASH" ] && {
        local arch=$(uname -m)
        _failcat "${ZIP_BASE_DIR} 目录下没有内核文件"
        _download_clash "$arch"
        ZIP_KERNEL=$ZIP_CLASH
        BIN_KERNEL=$BIN_CLASH
    }

    BIN_KERNEL_NAME=$(basename "$BIN_KERNEL")
    _okcat "使用内核：$BIN_KERNEL_NAME"
}

_get_random_port() {
    local randomPort=$(shuf -i 1024-65535 -n 1)
    ! _is_bind "$randomPort" && { echo "$randomPort" && return; }
    _get_random_port
}

function _get_proxy_port() {
    local mixed_port=$(sudo "$BIN_YQ" '.mixed-port // ""' $CLASH_CONFIG_RUNTIME)
    MIXED_PORT=${mixed_port:-7890}

    _is_already_in_use "$MIXED_PORT" "$BIN_KERNEL_NAME" && {
        local newPort=$(_get_random_port)
        local msg="代理端口${MIXED_PORT} 被占用 已更换为$newPort"
        sudo "$BIN_YQ" -i ".mixed-port = $newPort" $CLASH_CONFIG_RUNTIME
        MIXED_PORT=$newPort
        _failcat '⚠️' "$msg"
    }
}

function _get_ui_port() {
    local ext_addr=$(sudo "$BIN_YQ" '.external-controller // ""' $CLASH_CONFIG_RUNTIME)
    local ext_port=${ext_addr##*:}
    UI_PORT=${ext_port:-9090}

    _is_already_in_use "$UI_PORT" "$BIN_KERNEL_NAME" && {
        local newPort=$(_get_random_port)
        local msg="控制端口${UI_PORT} 被占用 已更换为$newPort"
        sudo "$BIN_YQ" -i ".external-controller = \"0.0.0.0:$newPort\"" $CLASH_CONFIG_RUNTIME
        UI_PORT=$newPort
        _failcat '⚠️' "$msg"
    }
}

_get_color() {
    local hex="${1#\#}"
    local r=$((16#${hex:0:2}))
    local g=$((16#${hex:2:2}))
    local b=$((16#${hex:4:2}))
    printf "\e[38;2;%d;%d;%dm" "$r" "$g" "$b"
}
_get_color_msg() {
    local color=$(_get_color "$1")
    local msg=$2
    local reset="\033[0m"
    printf "%b%s%b\n" "$color" "$msg" "$reset"
}

function _okcat() {
    local color=#c8d6e5
    local emoji=✅
    [ $# -gt 1 ] && emoji=$1 && shift
    local msg="${emoji} $1"
    _get_color_msg "$color" "$msg" && return 0
}

function _failcat() {
    local color=#fd79a8
    local emoji=❌
    [ $# -gt 1 ] && emoji=$1 && shift
    local msg="${emoji} $1"
    _get_color_msg "$color" "$msg" >&2 && return 1
}

function _quit() {
    local user=root
    [ -n "$SUDO_USER" ] && user=$SUDO_USER
    exec sudo -u "$user" -- "$_SHELL" -i
}

function _error_quit() {
    [ $# -gt 0 ] && {
        local color=#f92f60
        local emoji=💥
        [ $# -gt 1 ] && emoji=$1 && shift
        local msg="${emoji} $1"
        _get_color_msg "$color" "$msg"
    }
    exec $_SHELL -i
}

_is_bind() {
    local port=$1
    { sudo ss -lnptu || sudo netstat -lnptu; } | grep ":${port}\b"
}

_is_already_in_use() {
    local port=$1
    local progress=$2
    _is_bind "$port" | grep -qs -v "$progress"
}

function _is_root() {
    [ "$(whoami)" = "root" ]
}

function _valid_env() {
    _is_root || _error_quit "请使用 root 或 sudo 权限运行"
    [ -n "$ZSH_VERSION" ] && [ -n "$BASH_VERSION" ] && _error_quit "请不要同时使用bash和zsh"
    [ "$(ps -p 1 -o comm=)" != "systemd" ] && _error_quit "系统不支持 systemd"
}

function _valid_config() {
    [ -e "$1" ] && [ "$(wc -l <"$1")" -gt 1 ] && {
        local cmd msg
        cmd="$BIN_KERNEL -d $(dirname "$1") -f $1 -t"
        msg=$(eval "$cmd") || {
            eval "$cmd"
            echo "$msg" | grep -qs "unsupport proxy type" && _error_quit "配置包含不支持的代理类型 请使用 mihomo 内核"
        }
    }
}

_download_clash() {
    local arch=$1
    local url sha256sum
    case "$arch" in
    x86_64)
        url=https://downloads.clash.wiki/ClashPremium/clash-linux-amd64-2023.08.17.gz
        sha256sum='92380f053f083e3794c1681583be013a57b160292d1d9e1056e7fa1c2d948747'
        ;;
    *86*)
        url=https://downloads.clash.wiki/ClashPremium/clash-linux-386-2023.08.17.gz
        sha256sum='254125efa731ade3c1bf7cfd83ae09a824e1361592ccd7c0cccd2a266dcb92b5'
        ;;
    armv*)
        url=https://downloads.clash.wiki/ClashPremium/clash-linux-armv5-2023.08.17.gz
        sha256sum='622f5e774847782b6d54066f0716114a088f143f9bdd37edf3394ae8253062e8'
        ;;
    aarch64)
        url=https://downloads.clash.wiki/ClashPremium/clash-linux-arm64-2023.08.17.gz
        sha256sum='c45b39bb241e270ae5f4498e2af75cecc0f03c9db3c0db5e55c8c4919f01afdd'
        ;;
    *)
        _error_quit "不支持的架构$arch，请手动下载内核到 ${ZIP_BASE_DIR} 目录，下载地址：https://downloads.clash.wiki/ClashPremium/"
        ;;
    esac

    _okcat '📥' "正在下载clash内核${arch} 版本..."
    local clash_zip="${ZIP_BASE_DIR}/$(basename $url)"
    curl \
        --progress-bar \
        --show-error \
        --fail \
        --insecure \
        --connect-timeout 15 \
        --retry 1 \
        --output "$clash_zip" \
        "$url"
    echo $sha256sum "$clash_zip" | sha256sum -c ||
        _error_quit "校验失败，请手动下载到 ${ZIP_BASE_DIR} 目录，下载地址：https://downloads.clash.wiki/ClashPremium/"
}

_download_raw_config() {
    local dest=$1
    local url=$2
    local agent='clash-verge/v2.0.4'
    sudo curl \
        --silent \
        --show-error \
        --insecure \
        --connect-timeout 4 \
        --retry 1 \
        --user-agent "$agent" \
        --output "$dest" \
        "$url" ||
        sudo wget \
            --no-verbose \
            --no-check-certificate \
            --timeout 3 \
            --tries 1 \
            --user-agent "$agent" \
            --output-document "$dest" \
            "$url"
}
_download_convert_config() {
    local dest=$1
    local url=$2
    _start_convert
    local convert_url=$(
        target='clash'
        base_url="http://127.0.0.1:${BIN_SUBCONVERTER_PORT}/sub"
        curl \
            --get \
            --silent \
            --output /dev/null \
            --data-urlencode "target=$target" \
            --data-urlencode "url=$url" \
            --write-out '%{url_effective}' \
            "$base_url"
    )
    _download_raw_config "$dest" "$convert_url"
    _stop_convert
}
function _download_config() {
    local dest=$1
    local url=$2
    [ "${url:0:4}" = 'file' ] && return 0
    _download_raw_config "$dest" "$url" || return 1
    _okcat '🔍' '正在验证配置文件...'
    _valid_config "$dest" || {
        _failcat '⚠️' "配置验证失败，尝试转换..."
        _download_convert_config "$dest" "$url" || _failcat '❌' "配置转换失败，查看日志：$BIN_SUBCONVERTER_LOG"
    }
}

_start_convert() {
    _is_already_in_use $BIN_SUBCONVERTER_PORT 'subconverter' && {
        local newPort=$(_get_random_port)
        _failcat '⚠️' "转换端口$BIN_SUBCONVERTER_PORT 被占用 已更换为$newPort"
        [ ! -e "$BIN_SUBCONVERTER_CONFIG" ] && {
            sudo /bin/cp -f "$BIN_SUBCONVERTER_DIR/pref.example.yml" "$BIN_SUBCONVERTER_CONFIG"
        }
        sudo "$BIN_YQ" -i ".server.port = $newPort" "$BIN_SUBCONVERTER_CONFIG"
        BIN_SUBCONVERTER_PORT=$newPort
    }
    local start=$(date +%s)
    # 启动shell子进程避免kill影响主进程
    (sudo "$BIN_SUBCONVERTER" 2>&1 | sudo tee "$BIN_SUBCONVERTER_LOG" >/dev/null &)
    while ! _is_bind "$BIN_SUBCONVERTER_PORT" >&/dev/null; do
        sleep 1s
        local now=$(date +%s)
        [ $((now - start)) -gt 1 ] && _error_quit "订阅转换服务启动失败，查看日志：$BIN_SUBCONVERTER_LOG"
    done
}
_stop_convert() {
    pkill -9 -f "$BIN_SUBCONVERTER" >&/dev/null
}
