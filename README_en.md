# Easy Linux Command Line Proxy: clash-cli  

**Language**: [English](README_en.md) | [中文](README_zh.md)

![GitHub License](https://img.shields.io/github/license/whillhill/clash-cli)
![GitHub top language](https://img.shields.io/github/languages/top/whillhill/clash-cli)
![GitHub Repo stars](https://img.shields.io/github/stars/whillhill/clash-cli)
![PyPI](https://img.shields.io/pypi/v/clash-cli)
![Python](https://img.shields.io/pypi/pyversions/clash-cli)


**🎉 Supports two installation methods: Shell script and Python package!**


## ✨ Features

- 🚀 **One-click Installation**: Automatically download and configure Clash kernel
- 🔧 **Smart Management**: Unified `clash-cli` command line interface
- 🌐 **Subscription Conversion**: Built-in subconverter for local subscription conversion
- 🎯 **Multi-kernel Support**: Default mihomo, optional clash kernel
- 🐚 **Multi-shell Support**: Compatible with bash, zsh, fish
- 🔒 **System Integration**: systemd service management, auto-start on boot
- 🌍 **Web Console**: Visual node management and monitoring
- 📱 **Tun Mode**: Global proxy, supports Docker containers
- 🐍 **Python Support**: Modern pip installation method

## 📋 Requirements

- **Operating System**: Linux
- **User Permissions**: `root` or `sudo` privileges
- **Shell Environment**: Any of `bash`, `zsh`, `fish`

## 🚀 Quick Installation

> The two installation methods **differ only in installation process**, the **usage is completely identical** after installation!

### 📊 Installation Method Comparison

| Aspect | Python Package | Shell Script |
|--------|----------------|--------------|
| **Install Command** | `pip install clash-cli` | `git clone + bash install.sh` |
| **Dependency Management** | pip handles automatically | script handles manually |
| **Update Method** | `pip install -U clash-cli` | re-clone git |
| **Uninstall Method** | `pip uninstall clash-cli` | `bash uninstall.sh` |
| **Usage Commands** | ✅ **Completely Same** | ✅ **Completely Same** |

### Method 1: Python Package Installation (Recommended)

```bash
# 1. Install clash-cli tool
pip install clash-cli

# 2. Install Clash service (requires sudo)
sudo clash-cli install

# 3. Start using
clash-cli on
```


### Method 2: Shell Script Installation (Traditional)

```bash
git clone --branch main --depth 1 https://github.com/whillhill/clash-cli.git \
  && cd clash-cli \
  && sudo bash install.sh
```


## 📖 Usage Tutorial

> **Important**: Regardless of which installation method you use, all the following commands are **completely identical**!

### 🎯 Initial Configuration (Python Package Only)

If you use Python package installation, you need to install Clash service first:

```bash
# Install Clash service (requires sudo)
sudo clash-cli install

# Install with subscription URL
sudo clash-cli install -s "https://your-subscription-url.com"

# Use clash kernel (default is mihomo)
sudo clash-cli install --kernel clash
```

> **Note**: Shell script installation automatically completes service configuration during installation

### 📋 Basic Commands

After installation, **both installation methods use the same** `clash-cli` commands:

```bash
$ clash-cli
Usage:
    clash-cli COMMAND [OPTION]

Commands:
    on                   Enable proxy
    off                  Disable proxy
    ui                   Panel address
    status               Kernel status
    proxy    [on|off]    System proxy
    tun      [on|off]    Tun mode
    mixin    [-e|-r]     Mixin configuration
    secret   [SECRET]    Web secret
    update   [auto|log]  Update subscription
    lang     [zh|en]     Switch language
```

#### Start and Stop Proxy

```bash
# Start proxy service
$ clash-cli on
😼 Proxy environment enabled

# Stop proxy service
$ clash-cli off
😼 Proxy environment disabled

# Check service status
$ clash-cli status
● mihomo.service - mihomo Daemon, A[nother] Clash Kernel.
   Loaded: loaded (/etc/systemd/system/mihomo.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2025-01-27 10:30:15 CST; 2h 15min ago
```

**Description**:
- `clash-cli on` starts kernel service and sets system proxy environment variables
- `clash-cli off` stops service and clears proxy environment variables
- Service supports auto-start on boot, automatically restores proxy state after restart

### 🌐 Web Console

#### Access Console

```bash
$ clash-cli ui
╔═══════════════════════════════════════════════╗
║                😼 Web Console                 ║
║═══════════════════════════════════════════════║
║                                               ║
║     🔓 Note: Open port: 9090                  ║
║     🌍 Panel URL: http://127.0.0.1:9090/ui    ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

#### Security Settings

```bash
# Set access secret
$ clash-cli secret mypassword123
😼 Secret updated successfully, restarted

# View current secret
$ clash-cli secret
😼 Current secret: mypassword123

# Clear secret (set to empty)
$ clash-cli secret ""
😼 Secret updated successfully, restarted
```

### 📡 Subscription Management

#### Manual Subscription Update

```bash
# Update with new subscription URL
$ clash-cli update https://your-subscription-url.com
👌 Downloading: Original config backed up...
🍃 Download successful: Kernel validating config...
🍃 Subscription updated successfully

# Update with last subscription URL
$ clash-cli update
🍃 Subscription updated successfully

# View update log
$ clash-cli update log
✅ [2025-01-27 10:30:15] Subscription updated: https://your-subscription-url.com
✅ [2025-01-27 08:15:22] Subscription updated: https://your-subscription-url.com
```

#### Auto Update Settings

```bash
# Set auto update (every 2 days at midnight)
$ clash-cli update auto
😼 Scheduled subscription update set

# Set auto update with new subscription URL
$ clash-cli update auto https://new-subscription-url.com
😼 Scheduled subscription update set

# View scheduled tasks
$ crontab -l | grep clash-cli
0 0 */2 * * /bin/bash -i -c 'clash-cli update https://your-subscription-url.com'
```

### 🔧 Advanced Features

#### Tun Mode

```bash
# Check Tun status
$ clash-cli tun
😾 Tun status: disabled

# Enable Tun mode
$ clash-cli tun on
😼 Tun mode enabled

# Disable Tun mode
$ clash-cli tun off
😼 Tun mode disabled
```

#### Mixin Configuration Management

```bash
# View mixin configuration
$ clash-cli mixin
😼 less view mixin configuration

# Edit mixin configuration
$ clash-cli mixin -e
😼 vim edit mixin configuration

# View runtime configuration (merged final configuration)
$ clash-cli mixin -r
😼 less view runtime configuration
```

### 🌍 Language Switch

```bash
# Check current language
$ clash-cli lang
Current language: English (en)

# Switch to Chinese
$ clash-cli lang zh
语言已切换为中文

# Switch to English
$ clash-cli lang en
Language switched to English
```

## 🗑️ Uninstallation

### Uninstallation Method Comparison

| Installation Method | Uninstall Command | Description |
|---------------------|-------------------|-------------|
| **Python Package** | `pip uninstall clash-cli` | Uninstall clash-cli tool |
| **Shell Script** | `sudo bash uninstall.sh` | Run uninstall script |

### Complete Uninstallation Steps

**Regardless of installation method, stop service first**:

```bash
# 1. Stop proxy service
clash-cli off

# 2. Choose uninstall command based on installation method
# Python package method:
pip uninstall clash-cli

# Shell script method:
sudo bash uninstall.sh
```

> **Note**: After uninstallation, Clash service configuration and data will be completely removed

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the [MIT](LICENSE) License.

## ⭐ Star History

<a href="https://www.star-history.com/#whillhill/clash-cli&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date" />
 </picture>
</a>

## ⚠️ Disclaimer

This tool is for learning and research purposes only. Please comply with local laws and regulations. Users are responsible for any consequences arising from the use of this tool.
