"""
多语言支持模块
Internationalization (i18n) support module
"""

import os
from pathlib import Path
from typing import Dict, Any

# 配置文件路径（与 Shell 版本保持一致）
CLASH_LANG_CONF = "/opt/clash/lang.conf"

# 多语言消息字典
MESSAGES: Dict[str, Dict[str, str]] = {
    'zh': {
        # 代理状态消息
        'proxy_on': '😼 已开启代理环境',
        'proxy_off': '😼 已关闭代理环境',
        'proxy_enabled': '😼 系统代理：开启',
        'proxy_disabled': '😼 系统代理：关闭',
        
        # Tun 模式消息
        'tun_enabled': '😼 Tun 模式已开启',
        'tun_disabled': '😼 Tun 模式已关闭',
        'tun_status_on': '😼 Tun 状态：开启',
        'tun_status_off': '😾 Tun 状态：关闭',
        
        # 密钥管理消息
        'secret_updated': '😼 密钥更新成功，已重启生效',
        'current_secret': '😼 当前密钥：',
        
        # 订阅更新消息
        'update_success': '🍃 订阅更新成功',
        'update_downloading': '👌 正在下载：原配置已备份...',
        'update_validating': '🍃 下载成功：内核验证配置...',
        'auto_update_set': '😼 已设置定时更新订阅',
        
        # Mixin 配置消息
        'mixin_view': '😼 less 查看 mixin 配置',
        'mixin_edit': '😼 vim 编辑 mixin 配置',
        'mixin_runtime': '😼 less 查看 运行时 配置',
        'config_updated': '配置更新成功，已重启生效',
        
        # Web 控制台消息
        'web_console': '😼 Web 控制台',
        'note_open_port': '🔓 注意放行端口：9090',
        'panel_address': '🌍 面板地址：http://127.0.0.1:9090/ui',
        
        # 安装卸载消息
        'uninstalled': '✨ 已卸载，相关配置已清除',
        'enjoy': '🎉 enjoy 🎉',
        'installation_complete': '🎉 安装完成！',
        'service_started': '🚀 服务已启动',
        
        # 语言切换消息
        'lang_switched': '语言已切换为中文',
        'current_lang': '当前语言：中文 (zh)',
        'lang_usage': '用法: clash-cli lang [zh|en]',
        
        # 错误消息
        'error_permission': '❌ 权限不足，请使用 sudo 运行',
        'error_not_found': '❌ 文件未找到',
        'error_invalid_config': '❌ 配置文件无效',
        'error_service_failed': '❌ 服务启动失败',
        
        # 成功消息
        'success_installed': '✅ 安装成功',
        'success_started': '✅ 服务已启动',
        'success_stopped': '✅ 服务已停止',
        'success_updated': '✅ 更新成功',
        
        # 状态消息
        'status_running': '🟢 运行中',
        'status_stopped': '🔴 已停止',
        'status_unknown': '🟡 状态未知',
        
        # 帮助信息
        'help_install': '安装 Clash 服务',
        'help_uninstall': '卸载 Clash 服务',
        'help_on': '开启代理',
        'help_off': '关闭代理',
        'help_status': '查看服务状态',
        'help_ui': '显示 Web 控制台地址',
        'help_update': '更新订阅配置',
        'help_tun': '管理 Tun 模式',
        'help_mixin': '管理 Mixin 配置',
        'help_secret': '管理 Web 密钥',
        'help_lang': '切换语言',
    },
    'en': {
        # 代理状态消息
        'proxy_on': '😼 Proxy environment enabled',
        'proxy_off': '😼 Proxy environment disabled',
        'proxy_enabled': '😼 System proxy: enabled',
        'proxy_disabled': '😼 System proxy: disabled',
        
        # Tun 模式消息
        'tun_enabled': '😼 Tun mode enabled',
        'tun_disabled': '😼 Tun mode disabled',
        'tun_status_on': '😼 Tun status: enabled',
        'tun_status_off': '😾 Tun status: disabled',
        
        # 密钥管理消息
        'secret_updated': '😼 Secret updated successfully, restarted',
        'current_secret': '😼 Current secret: ',
        
        # 订阅更新消息
        'update_success': '🍃 Subscription updated successfully',
        'update_downloading': '👌 Downloading: Original config backed up...',
        'update_validating': '🍃 Download successful: Kernel validating config...',
        'auto_update_set': '😼 Scheduled subscription update set',
        
        # Mixin 配置消息
        'mixin_view': '😼 less view mixin configuration',
        'mixin_edit': '😼 vim edit mixin configuration',
        'mixin_runtime': '😼 less view runtime configuration',
        'config_updated': 'Configuration updated successfully, restarted',
        
        # Web 控制台消息
        'web_console': '😼 Web Console',
        'note_open_port': '🔓 Note: Open port: 9090',
        'panel_address': '🌍 Panel URL: http://127.0.0.1:9090/ui',
        
        # 安装卸载消息
        'uninstalled': '✨ Uninstalled, related configurations cleared',
        'enjoy': '🎉 enjoy 🎉',
        'installation_complete': '🎉 Installation complete!',
        'service_started': '🚀 Service started',
        
        # 语言切换消息
        'lang_switched': 'Language switched to English',
        'current_lang': 'Current language: English (en)',
        'lang_usage': 'Usage: clash-cli lang [zh|en]',
        
        # 错误消息
        'error_permission': '❌ Insufficient permissions, please run with sudo',
        'error_not_found': '❌ File not found',
        'error_invalid_config': '❌ Invalid configuration file',
        'error_service_failed': '❌ Service startup failed',
        
        # 成功消息
        'success_installed': '✅ Installation successful',
        'success_started': '✅ Service started',
        'success_stopped': '✅ Service stopped',
        'success_updated': '✅ Update successful',
        
        # 状态消息
        'status_running': '🟢 Running',
        'status_stopped': '🔴 Stopped',
        'status_unknown': '🟡 Unknown status',
        
        # 帮助信息
        'help_install': 'Install Clash service',
        'help_uninstall': 'Uninstall Clash service',
        'help_on': 'Enable proxy',
        'help_off': 'Disable proxy',
        'help_status': 'Show service status',
        'help_ui': 'Show Web console address',
        'help_update': 'Update subscription configuration',
        'help_tun': 'Manage Tun mode',
        'help_mixin': 'Manage Mixin configuration',
        'help_secret': 'Manage Web secret',
        'help_lang': 'Switch language',
    }
}


def get_current_lang() -> str:
    """获取当前语言设置"""
    try:
        if os.path.exists(CLASH_LANG_CONF):
            with open(CLASH_LANG_CONF, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                for line in content.split('\n'):
                    if line.startswith('LANG='):
                        lang = line.split('=', 1)[1].strip()
                        if lang in ['zh', 'en']:
                            return lang
    except Exception:
        pass
    return 'zh'  # 默认中文


def set_language(lang: str) -> bool:
    """设置语言并保存到配置文件"""
    if lang not in ['zh', 'en']:
        return False
    
    try:
        # 确保配置目录存在
        config_dir = os.path.dirname(CLASH_LANG_CONF)
        os.makedirs(config_dir, exist_ok=True)
        
        # 写入配置文件
        with open(CLASH_LANG_CONF, 'w', encoding='utf-8') as f:
            f.write(f'LANG={lang}\n')
        return True
    except Exception:
        return False


def _(key: str, **kwargs) -> str:
    """翻译函数"""
    current_lang = get_current_lang()
    message = MESSAGES.get(current_lang, MESSAGES['zh']).get(key, key)
    
    # 支持格式化参数
    if kwargs:
        try:
            return message.format(**kwargs)
        except (KeyError, ValueError):
            return message
    
    return message


def get_help_text(command: str = None) -> str:
    """获取帮助文本"""
    current_lang = get_current_lang()
    
    if current_lang == 'en':
        if command:
            return MESSAGES['en'].get(f'help_{command}', f'Help for {command}')
        else:
            return """Usage:
    clash-cli COMMAND [OPTION]

Commands:
    install              Install Clash service
    uninstall            Uninstall Clash service
    on                   Enable proxy
    off                  Disable proxy
    status               Show service status
    ui                   Show Web console address
    update               Update subscription configuration
    tun      [on|off]    Manage Tun mode
    mixin    [-e|-r]     Manage Mixin configuration
    secret   [SECRET]    Manage Web secret
    lang     [zh|en]     Switch language"""
    else:
        if command:
            return MESSAGES['zh'].get(f'help_{command}', f'{command} 的帮助')
        else:
            return """用法:
    clash-cli COMMAND [OPTION]

命令:
    install              安装 Clash 服务
    uninstall            卸载 Clash 服务
    on                   开启代理
    off                  关闭代理
    status               查看服务状态
    ui                   显示 Web 控制台地址
    update               更新订阅配置
    tun      [on|off]    管理 Tun 模式
    mixin    [-e|-r]     管理 Mixin 配置
    secret   [SECRET]    管理 Web 密钥
    lang     [zh|en]     切换语言"""
