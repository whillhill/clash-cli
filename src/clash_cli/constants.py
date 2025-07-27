"""
clash-cli 常量定义
"""

import os
from pathlib import Path

# 版本信息
VERSION = "1.0.0"

# 路径配置
CLASH_BASE_DIR = Path("/opt/clash")
CLASH_CONFIG_DIR = CLASH_BASE_DIR / "config"
CLASH_BIN_DIR = CLASH_BASE_DIR / "bin"
CLASH_LOG_DIR = CLASH_BASE_DIR / "logs"

# 配置文件路径
CLASH_CONFIG_RAW = CLASH_CONFIG_DIR / "config.yaml"
CLASH_CONFIG_MIXIN = CLASH_CONFIG_DIR / "mixin.yaml"
CLASH_CONFIG_RUNTIME = CLASH_CONFIG_DIR / "runtime.yaml"
CLASH_CONFIG_URL = CLASH_CONFIG_DIR / "url"
CLASH_UPDATE_LOG = CLASH_LOG_DIR / "update.log"

# 二进制文件路径
BIN_MIHOMO = CLASH_BIN_DIR / "mihomo"
BIN_CLASH = CLASH_BIN_DIR / "clash"
BIN_YQ = CLASH_BIN_DIR / "yq"
BIN_SUBCONVERTER_DIR = CLASH_BIN_DIR / "subconverter"
BIN_SUBCONVERTER = BIN_SUBCONVERTER_DIR / "subconverter"

# 系统服务
SYSTEMD_SERVICE_FILE = Path("/etc/systemd/system/mihomo.service")
SERVICE_NAME = "mihomo"

# 网络配置
DEFAULT_MIXED_PORT = 7890
DEFAULT_UI_PORT = 9090
DEFAULT_SUBCONVERTER_PORT = 25500

# Shell 配置文件
SHELL_RC_BASH = "~/.bashrc"
SHELL_RC_ZSH = "~/.zshrc"
SHELL_RC_FISH = "~/.config/fish/conf.d/clash-cli.fish"

# 下载链接
DOWNLOAD_URLS = {
    "mihomo": {
        "x86_64": "https://github.com/MetaCubeX/mihomo/releases/download/v1.19.2/mihomo-linux-amd64-compatible-v1.19.2.gz",
        "aarch64": "https://github.com/MetaCubeX/mihomo/releases/download/v1.19.2/mihomo-linux-arm64-v1.19.2.gz",
        "armv7": "https://github.com/MetaCubeX/mihomo/releases/download/v1.19.2/mihomo-linux-armv7-v1.19.2.gz",
    },
    "clash": {
        "x86_64": "https://downloads.clash.wiki/ClashPremium/clash-linux-amd64-2023.08.17.gz",
        "aarch64": "https://downloads.clash.wiki/ClashPremium/clash-linux-arm64-2023.08.17.gz",
        "armv7": "https://downloads.clash.wiki/ClashPremium/clash-linux-armv5-2023.08.17.gz",
    },
    "subconverter": "https://github.com/tindy2013/subconverter/releases/download/v0.9.0/subconverter_linux64.tar.gz",
    "yq": "https://github.com/mikefarah/yq/releases/download/v4.45.1/yq_linux_amd64.tar.gz",
    "yacd": "https://github.com/haishanh/yacd/releases/download/v0.3.8/yacd.tar.xz",
    "country_mmdb": "https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb",
}

# 代理环境变量
PROXY_ENV_VARS = [
    "http_proxy",
    "https_proxy", 
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "all_proxy",
    "ALL_PROXY",
    "no_proxy",
    "NO_PROXY",
]

# 支持的架构
SUPPORTED_ARCHITECTURES = ["x86_64", "aarch64", "armv7"]

# 支持的发行版
SUPPORTED_DISTROS = [
    "ubuntu",
    "debian", 
    "centos",
    "rhel",
    "fedora",
    "arch",
    "manjaro",
]

# 默认 Mixin 配置
DEFAULT_MIXIN_CONFIG = {
    "system-proxy": {"enable": True},
    "external-controller": f"0.0.0.0:{DEFAULT_UI_PORT}",
    "external-ui": "public",
    "secret": "",
    "allow-lan": False,
    "authentication": [],
    "rules": [
        "DOMAIN,api64.ipify.org,DIRECT",  # 用于获取公网 IP
    ],
    "tun": {
        "enable": False,
        "stack": "system",
        "auto-route": True,
        "auto-redir": True,
        "auto-redirect": True,
        "auto-detect-interface": True,
        "dns-hijack": ["any:53", "tcp://any:53"],
        "strict-route": True,
        "exclude-interface": [],
    },
    "dns": {
        "enable": True,
        "listen": "0.0.0.0:1053",
        "enhanced-mode": "fake-ip",
        "nameserver": ["114.114.114.114", "8.8.8.8"],
    },
}

# 用户代理
USER_AGENT = "clash-cli/1.0.0"

# 超时设置
DOWNLOAD_TIMEOUT = 30
REQUEST_TIMEOUT = 10
SERVICE_TIMEOUT = 30
