#!/bin/bash
# shellcheck disable=SC2148
# shellcheck disable=SC1091
. script/common.sh >&/dev/null
. script/clash-cli.sh >&/dev/null

_valid_env

clash-cli off >&/dev/null

systemctl disable "$BIN_KERNEL_NAME" >&/dev/null
rm -f "/etc/systemd/system/${BIN_KERNEL_NAME}.service"
systemctl daemon-reload

rm -rf "$CLASH_BASE_DIR"
rm -rf "$RESOURCES_BIN_DIR"
sed -i '/clash-cli update/d' "$CLASH_CRON_TAB" >&/dev/null
_set_rc unset

_okcat '✨' '已卸载，相关配置已清除'
_quit
