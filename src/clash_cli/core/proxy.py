"""
代理管理
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
import requests

from ..constants import (
    PROXY_ENV_VARS, DEFAULT_MIXED_PORT, DEFAULT_UI_PORT,
    CLASH_CONFIG_RUNTIME, SHELL_RC_BASH, SHELL_RC_ZSH, SHELL_RC_FISH
)
from ..exceptions import ConfigError, NetworkError
from ..utils import (
    success_message, error_message, info_message, get_shell_type,
    is_port_in_use
)


class ProxyManager:
    """代理管理器"""
    
    def __init__(self):
        self.mixed_port = DEFAULT_MIXED_PORT
        self.ui_port = DEFAULT_UI_PORT
        self._load_ports_from_config()
    
    def _load_ports_from_config(self) -> None:
        """从配置文件加载端口信息"""
        try:
            if CLASH_CONFIG_RUNTIME.exists():
                import yaml
                with open(CLASH_CONFIG_RUNTIME, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                
                self.mixed_port = config.get('mixed-port', DEFAULT_MIXED_PORT)
                
                # 解析 external-controller
                controller = config.get('external-controller', f'0.0.0.0:{DEFAULT_UI_PORT}')
                if ':' in controller:
                    self.ui_port = int(controller.split(':')[-1])
                    
        except Exception:
            # 如果加载失败，使用默认端口
            pass
    
    def get_proxy_info(self) -> Dict[str, str]:
        """获取代理信息"""
        auth = self._get_auth_string()
        auth_prefix = f"{auth}@" if auth else ""
        
        return {
            'http_proxy': f"http://{auth_prefix}127.0.0.1:{self.mixed_port}",
            'https_proxy': f"http://{auth_prefix}127.0.0.1:{self.mixed_port}",
            'socks_proxy': f"socks5h://{auth_prefix}127.0.0.1:{self.mixed_port}",
            'no_proxy': 'localhost,127.0.0.1,::1',
        }
    
    def _get_auth_string(self) -> Optional[str]:
        """获取认证字符串"""
        try:
            if CLASH_CONFIG_RUNTIME.exists():
                import yaml
                with open(CLASH_CONFIG_RUNTIME, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                
                auth_list = config.get('authentication', [])
                if auth_list and len(auth_list) > 0:
                    return auth_list[0]
            return None
        except Exception:
            return None
    
    def set_system_proxy(self) -> None:
        """设置系统代理环境变量"""
        proxy_info = self.get_proxy_info()
        
        # 设置环境变量
        os.environ['http_proxy'] = proxy_info['http_proxy']
        os.environ['https_proxy'] = proxy_info['https_proxy']
        os.environ['HTTP_PROXY'] = proxy_info['http_proxy']
        os.environ['HTTPS_PROXY'] = proxy_info['https_proxy']
        os.environ['all_proxy'] = proxy_info['socks_proxy']
        os.environ['ALL_PROXY'] = proxy_info['socks_proxy']
        os.environ['no_proxy'] = proxy_info['no_proxy']
        os.environ['NO_PROXY'] = proxy_info['no_proxy']
        
        success_message("已设置系统代理环境变量")
    
    def unset_system_proxy(self) -> None:
        """清除系统代理环境变量"""
        for var in PROXY_ENV_VARS:
            if var in os.environ:
                del os.environ[var]
        
        success_message("已清除系统代理环境变量")
    
    def get_proxy_status(self) -> Dict[str, any]:
        """获取代理状态"""
        proxy_info = self.get_proxy_info()
        
        # 检查环境变量
        env_set = all(var in os.environ for var in ['http_proxy', 'https_proxy'])
        
        # 检查端口占用
        port_in_use = is_port_in_use(self.mixed_port)
        
        return {
            'enabled': env_set,
            'port_in_use': port_in_use,
            'mixed_port': self.mixed_port,
            'ui_port': self.ui_port,
            'proxy_info': proxy_info,
            'env_vars': {var: os.environ.get(var, '') for var in PROXY_ENV_VARS}
        }
    
    def test_proxy_connection(self) -> bool:
        """测试代理连接"""
        try:
            proxy_info = self.get_proxy_info()
            proxies = {
                'http': proxy_info['http_proxy'],
                'https': proxy_info['http_proxy']
            }
            
            # 测试连接
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_public_ip(self, use_proxy: bool = False) -> Optional[str]:
        """获取公网 IP"""
        try:
            proxies = None
            if use_proxy:
                proxy_info = self.get_proxy_info()
                proxies = {
                    'http': proxy_info['http_proxy'],
                    'https': proxy_info['http_proxy']
                }
            
            response = requests.get(
                'http://api64.ipify.org',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.text.strip()
            
            return None
            
        except Exception:
            return None
    
    def get_ui_info(self) -> Dict[str, str]:
        """获取 Web UI 信息"""
        try:
            # 获取本地 IP
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # 获取公网 IP
            public_ip = self.get_public_ip(use_proxy=False)
            
            # 获取密钥
            secret = self._get_ui_secret()
            
            ui_info = {
                'port': str(self.ui_port),
                'local_url': f"http://{local_ip}:{self.ui_port}/ui",
                'public_url': f"http://{public_ip or '公网IP'}:{self.ui_port}/ui",
                'cloud_url': "http://board.zash.run.place",
                'secret': secret or "无",
            }
            
            return ui_info
            
        except Exception as e:
            raise ConfigError(f"获取 UI 信息失败: {e}")
    
    def _get_ui_secret(self) -> Optional[str]:
        """获取 UI 密钥"""
        try:
            if CLASH_CONFIG_RUNTIME.exists():
                import yaml
                with open(CLASH_CONFIG_RUNTIME, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                return config.get('secret', '')
            return None
        except Exception:
            return None
    
    def set_ui_secret(self, secret: str) -> None:
        """设置 UI 密钥"""
        from .config import ClashConfig
        
        config_manager = ClashConfig()
        config_manager.update_mixin_config({'secret': secret})
        config_manager.merge_configs()
        
        success_message("Web 控制台密钥设置成功")
    
    def enable_tun_mode(self) -> None:
        """启用 Tun 模式"""
        from .config import ClashConfig
        
        config_manager = ClashConfig()
        config_manager.update_mixin_config({
            'tun': {'enable': True}
        })
        config_manager.merge_configs()
        
        success_message("Tun 模式已启用")
    
    def disable_tun_mode(self) -> None:
        """禁用 Tun 模式"""
        from .config import ClashConfig
        
        config_manager = ClashConfig()
        config_manager.update_mixin_config({
            'tun': {'enable': False}
        })
        config_manager.merge_configs()
        
        success_message("Tun 模式已禁用")
    
    def get_tun_status(self) -> bool:
        """获取 Tun 模式状态"""
        try:
            if CLASH_CONFIG_RUNTIME.exists():
                import yaml
                with open(CLASH_CONFIG_RUNTIME, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                
                tun_config = config.get('tun', {})
                return tun_config.get('enable', False)
            
            return False
            
        except Exception:
            return False
    
    def setup_shell_integration(self) -> None:
        """设置 Shell 集成"""
        shell_type = get_shell_type()
        
        if shell_type == 'bash':
            self._setup_bash_integration()
        elif shell_type == 'zsh':
            self._setup_zsh_integration()
        elif shell_type == 'fish':
            self._setup_fish_integration()
    
    def _setup_bash_integration(self) -> None:
        """设置 Bash 集成"""
        rc_file = Path.home() / '.bashrc'
        self._add_shell_functions(rc_file, 'bash')
    
    def _setup_zsh_integration(self) -> None:
        """设置 Zsh 集成"""
        rc_file = Path.home() / '.zshrc'
        self._add_shell_functions(rc_file, 'zsh')
    
    def _setup_fish_integration(self) -> None:
        """设置 Fish 集成"""
        config_dir = Path.home() / '.config/fish/conf.d'
        config_dir.mkdir(parents=True, exist_ok=True)
        rc_file = config_dir / 'clash-cli.fish'
        self._add_shell_functions(rc_file, 'fish')
    
    def _add_shell_functions(self, rc_file: Path, shell_type: str) -> None:
        """添加 Shell 函数"""
        try:
            # 这里可以添加一些便捷的 shell 函数
            # 比如自动设置代理环境变量的函数
            functions = self._get_shell_functions(shell_type)
            
            # 检查是否已经添加过
            if rc_file.exists():
                with open(rc_file, 'r') as f:
                    content = f.read()
                if 'clash-cli integration' in content:
                    return
            
            # 添加函数
            with open(rc_file, 'a') as f:
                f.write('\n# clash-cli integration\n')
                f.write(functions)
                f.write('\n')
            
            success_message(f"已设置 {shell_type} 集成")
            
        except Exception as e:
            error_message(f"设置 {shell_type} 集成失败: {e}")
    
    def _get_shell_functions(self, shell_type: str) -> str:
        """获取 Shell 函数定义"""
        if shell_type == 'fish':
            return '''
function clash-proxy-on
    set -gx http_proxy http://127.0.0.1:7890
    set -gx https_proxy http://127.0.0.1:7890
    set -gx HTTP_PROXY http://127.0.0.1:7890
    set -gx HTTPS_PROXY http://127.0.0.1:7890
    set -gx all_proxy socks5h://127.0.0.1:7890
    set -gx ALL_PROXY socks5h://127.0.0.1:7890
    set -gx no_proxy localhost,127.0.0.1,::1
    set -gx NO_PROXY localhost,127.0.0.1,::1
    echo "😼 已设置代理环境变量"
end

function clash-proxy-off
    set -e http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
    set -e all_proxy ALL_PROXY no_proxy NO_PROXY
    echo "😼 已清除代理环境变量"
end
'''
        else:
            return '''
clash-proxy-on() {
    export http_proxy=http://127.0.0.1:7890
    export https_proxy=http://127.0.0.1:7890
    export HTTP_PROXY=http://127.0.0.1:7890
    export HTTPS_PROXY=http://127.0.0.1:7890
    export all_proxy=socks5h://127.0.0.1:7890
    export ALL_PROXY=socks5h://127.0.0.1:7890
    export no_proxy=localhost,127.0.0.1,::1
    export NO_PROXY=localhost,127.0.0.1,::1
    echo "😼 已设置代理环境变量"
}

clash-proxy-off() {
    unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
    unset all_proxy ALL_PROXY no_proxy NO_PROXY
    echo "😼 已清除代理环境变量"
}
'''
