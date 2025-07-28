#!/usr/bin/env python3
"""
clash-cli 主入口文件 - 极简版本，只提供 init 功能
"""

import sys
import click
from pathlib import Path

from . import __version__
from .init import ClashInitializer


def check_environment():
    """检查基本运行环境"""
    # 检查操作系统
    if sys.platform != 'linux':
        click.echo("❌ clash-cli 仅支持 Linux 系统", err=True)
        sys.exit(1)

    # 检查 Python 版本
    if sys.version_info < (3, 8):
        click.echo("❌ 需要 Python 3.8 或更高版本", err=True)
        sys.exit(1)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='显示版本信息')
@click.pass_context
def cli(ctx, version):
    """clash-cli - Linux Clash 代理工具快速安装器

    一键安装和管理 Clash 代理服务。
    """
    if version:
        click.echo(f"clash-cli version {__version__}")
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--subscription', '-s', help='订阅链接')
def install(subscription):
    """安装 Clash 代理服务

    自动下载、配置并启动 Clash 服务。
    """
    try:
        check_environment()

        initializer = ClashInitializer(mode='install', subscription=subscription)
        initializer.run()

    except KeyboardInterrupt:
        click.echo("\n❌ 操作被用户中断", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ 安装失败: {e}", err=True)
        sys.exit(1)


@cli.command()
def uninstall():
    """卸载 Clash 代理服务

    完全移除 Clash 服务和相关配置。
    """
    try:
        check_environment()

        if not click.confirm('确定要卸载 Clash 吗？这将删除所有配置文件'):
            click.echo("取消卸载")
            return

        initializer = ClashInitializer(mode='uninstall')
        initializer.run()

    except KeyboardInterrupt:
        click.echo("\n❌ 操作被用户中断", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ 卸载失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--target-dir', default='/tmp/clash-cli',
              help='脚本部署目录 (默认: /tmp/clash-cli)')
@click.option('--force', is_flag=True,
              help='强制覆盖已存在的目录')
def init(target_dir, force):
    """初始化 Clash 环境

    将打包的脚本和资源文件部署到指定目录，供手动使用。
    """
    try:
        check_environment()

        initializer = ClashInitializer(mode='init', target_dir=target_dir, force=force)
        initializer.run()

    except KeyboardInterrupt:
        click.echo("\n❌ 操作被用户中断", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ 初始化失败: {e}", err=True)
        sys.exit(1)


# 代理控制命令
@cli.command()
def on():
    """开启代理"""
    _call_shell_script('on')


@cli.command()
def off():
    """关闭代理"""
    _call_shell_script('off')


@cli.command()
def status():
    """查看服务状态"""
    _call_shell_script('status')


@cli.command()
def restart():
    """重启服务"""
    _call_shell_script('off')
    _call_shell_script('on')


@cli.command()
def ui():
    """显示 Web 控制台信息"""
    _call_shell_script('ui')


# 配置管理命令
@cli.group(invoke_without_command=True)
@click.pass_context
def proxy(ctx):
    """系统代理管理"""
    if ctx.invoked_subcommand is None:
        _call_shell_script('proxy')


@proxy.command()
def on():
    """开启系统代理"""
    _call_shell_script('proxy', 'on')


@proxy.command()
def off():
    """关闭系统代理"""
    _call_shell_script('proxy', 'off')


@cli.group(invoke_without_command=True)
@click.pass_context
def tun(ctx):
    """Tun 模式管理"""
    if ctx.invoked_subcommand is None:
        _call_shell_script('tun')


@tun.command()
def on():
    """开启 Tun 模式"""
    _call_shell_script('tun', 'on')


@tun.command()
def off():
    """关闭 Tun 模式"""
    _call_shell_script('tun', 'off')


@cli.command()
@click.argument('secret', required=False)
def secret(secret):
    """设置或查看 Web 控制台密钥"""
    if secret:
        _call_shell_script('secret', secret)
    else:
        _call_shell_script('secret')


# 订阅管理命令
@cli.group(invoke_without_command=True)
@click.pass_context
def update(ctx):
    """订阅管理"""
    if ctx.invoked_subcommand is None:
        _call_shell_script('update')


@update.command()
@click.argument('url', required=False)
def sync(url):
    """更新订阅"""
    if url:
        _call_shell_script('update', url)
    else:
        _call_shell_script('update')


@update.command()
def auto():
    """设置自动更新"""
    _call_shell_script('update', 'auto')


@update.command()
def log():
    """查看更新日志"""
    _call_shell_script('update', 'log')


# 配置文件管理
@cli.group(invoke_without_command=True)
@click.pass_context
def mixin(ctx):
    """Mixin 配置管理"""
    if ctx.invoked_subcommand is None:
        _call_shell_script('mixin')


@mixin.command()
def edit():
    """编辑 Mixin 配置"""
    _call_shell_script('mixin', '-e')


@mixin.command()
def runtime():
    """查看运行时配置"""
    _call_shell_script('mixin', '-r')


@cli.command()
@click.argument('language', required=False)
def lang(language):
    """切换语言"""
    if language:
        _call_shell_script('lang', language)
    else:
        _call_shell_script('lang')


def _call_shell_script(command, *args):
    """调用已安装的 shell 脚本"""
    import subprocess
    import os

    # 检查是否已安装
    clash_script = '/opt/clash/script/clash-cli.sh'
    if not os.path.exists(clash_script):
        click.echo("❌ Clash 未安装，请先运行: sudo clash-cli install", err=True)
        sys.exit(1)

    # 构建命令
    cmd_args = ['clash-cli', command] + list(args)

    try:
        # 调用 shell 脚本
        result = subprocess.run(cmd_args, check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        click.echo("❌ clash-cli 命令未找到，请检查安装", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 执行命令失败: {e}", err=True)
        sys.exit(1)


def main():
    """主函数"""
    cli()


if __name__ == '__main__':
    main()
