# clash-cli

![PyPI](https://img.shields.io/pypi/v/clash-cli)
![Python](https://img.shields.io/pypi/pyversions/clash-cli)
![License](https://img.shields.io/pypi/l/clash-cli)

Linux 一键安装 Clash 代理工具的 Python 实现版本。

## ✨ 特性

- 🚀 **一键安装**：`pip install clash-cli` 即可安装
- 🔧 **统一管理**：完整的命令行界面
- 🌐 **订阅转换**：内置订阅转换功能
- 🎯 **多内核支持**：支持 mihomo 和 clash 内核
- 🔒 **系统集成**：systemd 服务管理
- 🌍 **Web 控制台**：可视化管理界面
- 📱 **Tun 模式**：全局代理支持

## 📦 安装

```bash
pip install clash-cli
```

## 🚀 快速开始

### 1. 安装 Clash

```bash
# 使用默认 mihomo 内核安装
sudo clash-cli install

# 指定订阅链接安装
sudo clash-cli install -s "https://your-subscription-url.com"

# 使用 clash 内核安装
sudo clash-cli install --kernel clash
```

### 2. 基本使用

```bash
# 开启代理
clash-cli on

# 关闭代理
clash-cli off

# 查看状态
clash-cli status

# 查看 Web 控制台
clash-cli ui
```

## 📖 命令参考

### 基本命令

```bash
clash-cli install [--kernel mihomo|clash] [-s SUBSCRIPTION]  # 安装
clash-cli uninstall                                          # 卸载
clash-cli on                                                 # 开启代理
clash-cli off                                                # 关闭代理
clash-cli status [-n LINES] [-f]                            # 查看状态
clash-cli ui                                                 # Web 控制台信息
clash-cli info                                               # 系统信息
```

### 系统代理管理

```bash
clash-cli proxy          # 查看代理状态
clash-cli proxy on       # 开启系统代理
clash-cli proxy off      # 关闭系统代理
```

### Web 控制台

```bash
clash-cli secret [PASSWORD]    # 设置/查看密钥
```

### Tun 模式

```bash
clash-cli tun            # 查看 Tun 状态
clash-cli tun on         # 开启 Tun 模式
clash-cli tun off        # 关闭 Tun 模式
```

### 订阅管理

```bash
clash-cli update                    # 查看当前订阅
clash-cli update sync [URL]        # 更新订阅
clash-cli update log [-n LINES]    # 查看更新日志
```

### 配置管理

```bash
clash-cli mixin          # 查看 Mixin 配置
clash-cli mixin edit     # 编辑 Mixin 配置
clash-cli mixin runtime  # 查看运行时配置
```

## 🔧 高级配置

### Mixin 配置

Mixin 配置允许您自定义 Clash 设置，这些设置会与订阅配置合并：

```yaml
# 系统代理
system-proxy:
  enable: true

# Web 控制台
external-controller: "0.0.0.0:9090"
secret: "your-password"

# 自定义规则
rules:
  - DOMAIN-SUFFIX,example.com,DIRECT
  - DOMAIN-KEYWORD,google,PROXY

# Tun 模式
tun:
  enable: true
  stack: system
```

### 环境要求

- **操作系统**：Linux (支持 systemd)
- **Python**：3.8+
- **权限**：root 或 sudo
- **架构**：x86_64, aarch64, armv7

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [mihomo](https://github.com/MetaCubeX/mihomo) - Clash 内核
- [subconverter](https://github.com/tindy2013/subconverter) - 订阅转换
- [yacd](https://github.com/haishanh/yacd) - Web 控制台
- [click](https://click.palletsprojects.com/) - 命令行框架
- [rich](https://rich.readthedocs.io/) - 终端美化

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by [whillhill](https://github.com/whillhill)

</div>
