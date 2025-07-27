# linux命令行轻松使用代理：clash-cli  

**Language**: [English](README_en.md) | [中文](README_zh.md)

![GitHub License](https://img.shields.io/github/license/whillhill/clash-cli)
![GitHub top language](https://img.shields.io/github/languages/top/whillhill/clash-cli)
![GitHub Repo stars](https://img.shields.io/github/stars/whillhill/clash-cli)
![PyPI](https://img.shields.io/pypi/v/clash-cli)
![Python](https://img.shields.io/pypi/pyversions/clash-cli)


**🎉 支持两种安装方式：Shell 脚本和 Python 包！**


## ✨ 特性

- 🚀 **一键安装**：自动下载并配置 Clash 内核
- 🔧 **智能管理**：统一的 `clash-cli` 命令行界面
- 🌐 **订阅转换**：内置 subconverter 本地订阅转换
- 🎯 **多内核支持**：默认 mihomo，可选 clash 内核
- 🐚 **多 Shell 支持**：兼容 bash、zsh、fish
- 🔒 **系统集成**：systemd 服务管理，开机自启
- 🌍 **Web 控制台**：可视化节点管理和监控
- 📱 **Tun 模式**：全局代理，支持 Docker 容器
- 🐍 **Python 支持**：现代化的 pip 安装方式

## 📋 环境要求

- **操作系统**：Linux
- **用户权限**：`root` 或 `sudo` 权限
- **Shell 环境**：`bash`、`zsh`、`fish` 任一

## 🚀 快速安装

> 两种安装方式**仅安装方法不同**，安装完成后的**使用方式完全相同**！

### 📊 安装方式对比

| 方面 | Python 包安装 | Shell 脚本安装 |
|------|---------------|----------------|
| **安装命令** | `pip install clash-cli` | `git clone + bash install.sh` |
| **依赖管理** | pip 自动处理 | 脚本手动处理 |
| **更新方式** | `pip install -U clash-cli` | 重新 git clone |
| **卸载方式** | `pip uninstall clash-cli` | `bash uninstall.sh` |
| **使用命令** | ✅ **完全相同** | ✅ **完全相同** |

### 方式一：Python 包安装（推荐）

```bash
# 1. 安装 clash-cli 工具
pip install clash-cli

# 2. 安装 Clash 服务（需要 sudo 权限）
sudo clash-cli install

# 3. 开始使用
clash-cli on
```


### 方式二：Shell 脚本安装（传统方式）

```bash
git clone --branch main --depth 1 https://github.com/whillhill/clash-cli.git \
  && cd clash-cli \
  && sudo bash install.sh
```


## 📖 使用教程

> **重要**：无论使用哪种方式安装，以下所有命令都**完全相同**！

### 🎯 首次配置（仅 Python 包需要）

如果您使用 Python 包安装，需要先安装 Clash 服务：

```bash
# 安装 Clash 服务（需要 sudo 权限）
sudo clash-cli install

# 指定订阅链接安装
sudo clash-cli install -s "https://your-subscription-url.com"

# 使用 clash 内核（默认是 mihomo）
sudo clash-cli install --kernel clash
```

> **说明**：Shell 脚本安装会在安装过程中自动完成服务配置

### 📋 基本命令

安装完成后，**两种安装方式都使用相同的** `clash-cli` 命令：

```bash
$ clash-cli
Usage:
    clash-cli COMMAND [OPTION]

Commands:
    on                   开启代理
    off                  关闭代理
    ui                   面板地址
    status               内核状况
    proxy    [on|off]    系统代理
    tun      [on|off]    Tun 模式
    mixin    [-e|-r]     Mixin 配置
    secret   [SECRET]    Web 密钥
    update   [auto|log]  更新订阅
    lang     [zh|en]     切换语言
```

#### 启动和停止代理

```bash
# 启动代理服务
$ clash-cli on
😼 已开启代理环境

# 停止代理服务
$ clash-cli off
😼 已关闭代理环境

# 查看服务状态
$ clash-cli status
● mihomo.service - mihomo Daemon, A[nother] Clash Kernel.
   Loaded: loaded (/etc/systemd/system/mihomo.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2025-01-27 10:30:15 CST; 2h 15min ago
```

**说明**：
- `clash-cli on` 会同时启动内核服务和设置系统代理环境变量
- `clash-cli off` 会停止服务并清除代理环境变量
- 服务支持开机自启，重启后自动恢复代理状态

### 🌐 Web 控制台

#### 访问控制台

```bash
$ clash-cli ui
╔═══════════════════════════════════════════════╗
║                😼 Web 控制台                  ║
║═══════════════════════════════════════════════║
║                                               ║
║     🔓 注意放行端口：9090                      ║
║     🌍 面板地址：http://127.0.0.1:9090/ui     ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

#### 安全设置

```bash
# 设置访问密钥
$ clash-cli secret mypassword123
😼 密钥更新成功，已重启生效

# 查看当前密钥
$ clash-cli secret
😼 当前密钥：mypassword123

# 清除密钥（设为空）
$ clash-cli secret ""
😼 密钥更新成功，已重启生效
```

### 📡 订阅管理

#### 手动更新订阅

```bash
# 使用新的订阅链接更新
$ clash-cli update https://your-subscription-url.com
👌 正在下载：原配置已备份...
🍃 下载成功：内核验证配置...
🍃 订阅更新成功

# 使用上次的订阅链接更新
$ clash-cli update
🍃 订阅更新成功

# 查看更新日志
$ clash-cli update log
✅ [2025-01-27 10:30:15] 订阅更新成功：https://your-subscription-url.com
✅ [2025-01-27 08:15:22] 订阅更新成功：https://your-subscription-url.com
```

#### 自动更新设置

```bash
# 设置自动更新（每2天凌晨更新）
$ clash-cli update auto
😼 已设置定时更新订阅

# 设置自动更新并指定新的订阅链接
$ clash-cli update auto https://new-subscription-url.com
😼 已设置定时更新订阅

# 查看定时任务
$ crontab -l | grep clash-cli
0 0 */2 * * /bin/bash -i -c 'clash-cli update https://your-subscription-url.com'
```

### 🔧 高级功能

#### Tun 模式

```bash
# 查看 Tun 状态
$ clash-cli tun
😾 Tun 状态：关闭

# 开启 Tun 模式
$ clash-cli tun on
😼 Tun 模式已开启

# 关闭 Tun 模式
$ clash-cli tun off
😼 Tun 模式已关闭
```

#### Mixin 配置管理

```bash
# 查看 mixin 配置
$ clash-cli mixin
😼 less 查看 mixin 配置

# 编辑 mixin 配置
$ clash-cli mixin -e
😼 vim 编辑 mixin 配置

# 查看运行时配置（合并后的最终配置）
$ clash-cli mixin -r
😼 less 查看 运行时 配置
```

### 🌍 语言切换

```bash
# 查看当前语言
$ clash-cli lang
当前语言：中文 (zh)

# 切换到英文
$ clash-cli lang en
Language switched to English

# 切换到中文
$ clash-cli lang zh
语言已切换为中文
```

## 🗑️ 卸载

### 卸载方式对比

| 安装方式 | 卸载命令 | 说明 |
|----------|----------|------|
| **Python 包** | `pip uninstall clash-cli` | 卸载 clash-cli 工具 |
| **Shell 脚本** | `sudo bash uninstall.sh` | 运行卸载脚本 |

### 完整卸载步骤

**无论哪种安装方式，都需要先停止服务**：

```bash
# 1. 停止代理服务
clash-cli off

# 2. 根据安装方式选择卸载命令
# Python 包方式：
pip uninstall clash-cli

# Shell 脚本方式：
sudo bash uninstall.sh
```

> **注意**：卸载后 Clash 服务配置和数据会被完全清除

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

## ⭐ Star History

<a href="https://www.star-history.com/#whillhill/clash-cli&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=whillhill/clash-cli&type=Date" />
 </picture>
</a>

## ⚠️ 免责声明

本工具仅供学习和研究使用，请遵守当地法律法规。使用本工具所产生的任何后果由用户自行承担。
