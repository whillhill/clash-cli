"""
Clash 配置管理
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
import requests

from ..constants import (
    CLASH_CONFIG_RAW, CLASH_CONFIG_MIXIN, CLASH_CONFIG_RUNTIME,
    CLASH_CONFIG_URL, CLASH_UPDATE_LOG, DEFAULT_MIXIN_CONFIG,
    BIN_SUBCONVERTER, BIN_SUBCONVERTER_DIR, DEFAULT_SUBCONVERTER_PORT,
    USER_AGENT, REQUEST_TIMEOUT
)
from ..exceptions import ConfigError, NetworkError
from ..utils import (
    check_root_permission, run_command, success_message, 
    error_message, info_message, is_port_in_use, find_free_port
)


class ClashConfig:
    """Clash 配置管理器"""
    
    def __init__(self):
        self.config_raw = CLASH_CONFIG_RAW
        self.config_mixin = CLASH_CONFIG_MIXIN
        self.config_runtime = CLASH_CONFIG_RUNTIME
        self.config_url_file = CLASH_CONFIG_URL
        self.update_log = CLASH_UPDATE_LOG
        
        # 确保目录存在
        for config_file in [self.config_raw, self.config_mixin, self.config_runtime]:
            config_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """加载 YAML 配置文件"""
        try:
            if not file_path.exists():
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigError(f"加载配置文件失败 {file_path}: {e}")
    
    def save_yaml(self, data: Dict[str, Any], file_path: Path) -> None:
        """保存 YAML 配置文件"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
        except Exception as e:
            raise ConfigError(f"保存配置文件失败 {file_path}: {e}")
    
    def validate_config(self, config_path: Path) -> bool:
        """验证配置文件"""
        try:
            if not config_path.exists():
                return False
            
            # 检查文件大小
            if config_path.stat().st_size < 10:
                return False
            
            # 尝试加载 YAML
            config = self.load_yaml(config_path)
            
            # 基本验证
            required_fields = ['proxies', 'proxy-groups', 'rules']
            for field in required_fields:
                if field not in config:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def init_mixin_config(self) -> None:
        """初始化 Mixin 配置"""
        if not self.config_mixin.exists():
            self.save_yaml(DEFAULT_MIXIN_CONFIG, self.config_mixin)
            success_message("已创建默认 Mixin 配置")
    
    def get_mixin_config(self) -> Dict[str, Any]:
        """获取 Mixin 配置"""
        return self.load_yaml(self.config_mixin)
    
    def update_mixin_config(self, updates: Dict[str, Any]) -> None:
        """更新 Mixin 配置"""
        check_root_permission()
        
        try:
            current_config = self.get_mixin_config()
            
            # 深度合并配置
            def deep_merge(base: Dict, updates: Dict) -> Dict:
                result = base.copy()
                for key, value in updates.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = deep_merge(result[key], value)
                    else:
                        result[key] = value
                return result
            
            merged_config = deep_merge(current_config, updates)
            self.save_yaml(merged_config, self.config_mixin)
            success_message("Mixin 配置更新成功")
            
        except Exception as e:
            raise ConfigError(f"更新 Mixin 配置失败: {e}")
    
    def merge_configs(self) -> None:
        """合并配置文件生成运行时配置"""
        try:
            # 加载原始配置和 Mixin 配置
            raw_config = self.load_yaml(self.config_raw)
            mixin_config = self.load_yaml(self.config_mixin)
            
            if not raw_config:
                raise ConfigError("原始配置文件为空或不存在")
            
            # 深度合并配置
            def deep_merge(base: Dict, overlay: Dict) -> Dict:
                result = base.copy()
                for key, value in overlay.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = deep_merge(result[key], value)
                    elif key in result and isinstance(result[key], list) and isinstance(value, list):
                        # 对于列表，Mixin 的内容会添加到原配置前面
                        result[key] = value + result[key]
                    else:
                        result[key] = value
                return result
            
            # 合并配置
            runtime_config = deep_merge(raw_config, mixin_config)
            
            # 保存运行时配置
            self.save_yaml(runtime_config, self.config_runtime)
            success_message("配置合并成功")
            
        except Exception as e:
            raise ConfigError(f"合并配置失败: {e}")
    
    def download_config(self, url: str) -> None:
        """下载配置文件"""
        check_root_permission()
        
        try:
            # 备份当前配置
            if self.config_raw.exists():
                backup_path = self.config_raw.with_suffix('.yaml.bak')
                shutil.copy2(self.config_raw, backup_path)
                info_message("已备份原配置")
            
            # 尝试直接下载
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # 保存配置
            with open(self.config_raw, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # 验证配置
            if self.validate_config(self.config_raw):
                success_message("配置下载成功")
                # 保存订阅链接
                with open(self.config_url_file, 'w') as f:
                    f.write(url)
            else:
                # 如果直接下载的配置无效，尝试订阅转换
                info_message("配置验证失败，尝试订阅转换...")
                self._convert_subscription(url)
                
        except requests.RequestException as e:
            raise NetworkError(f"下载配置失败: {e}")
        except Exception as e:
            raise ConfigError(f"处理配置失败: {e}")
    
    def _convert_subscription(self, url: str) -> None:
        """使用 subconverter 转换订阅"""
        if not BIN_SUBCONVERTER.exists():
            raise ConfigError("subconverter 未安装")
        
        try:
            # 启动 subconverter
            port = DEFAULT_SUBCONVERTER_PORT
            if is_port_in_use(port):
                port = find_free_port(25500, 26000)
                info_message(f"端口 {DEFAULT_SUBCONVERTER_PORT} 被占用，使用端口 {port}")
            
            # 启动转换服务
            import subprocess
            import time
            
            process = subprocess.Popen(
                [str(BIN_SUBCONVERTER)],
                cwd=BIN_SUBCONVERTER_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服务启动
            time.sleep(3)
            
            try:
                # 构建转换 URL
                convert_url = f"http://127.0.0.1:{port}/sub"
                params = {
                    'target': 'clash',
                    'url': url,
                    'config': 'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini'
                }
                
                # 请求转换
                response = requests.get(convert_url, params=params, timeout=30)
                response.raise_for_status()
                
                # 保存转换后的配置
                with open(self.config_raw, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # 验证配置
                if self.validate_config(self.config_raw):
                    success_message("订阅转换成功")
                    # 保存订阅链接
                    with open(self.config_url_file, 'w') as f:
                        f.write(url)
                else:
                    raise ConfigError("转换后的配置验证失败")
                    
            finally:
                # 停止转换服务
                process.terminate()
                process.wait(timeout=5)
                
        except Exception as e:
            raise ConfigError(f"订阅转换失败: {e}")
    
    def update_subscription(self, url: Optional[str] = None) -> None:
        """更新订阅"""
        check_root_permission()
        
        try:
            # 如果没有提供 URL，尝试从文件读取
            if not url:
                if self.config_url_file.exists():
                    with open(self.config_url_file, 'r') as f:
                        url = f.read().strip()
                else:
                    raise ConfigError("未找到订阅链接，请提供 URL")
            
            if not url:
                raise ConfigError("订阅链接为空")
            
            info_message(f"正在更新订阅: {url}")
            
            # 下载新配置
            self.download_config(url)
            
            # 合并配置
            self.merge_configs()
            
            # 记录更新日志
            self._log_update(url, True)
            
            success_message("订阅更新成功")
            
        except Exception as e:
            self._log_update(url or "unknown", False, str(e))
            raise ConfigError(f"更新订阅失败: {e}")
    
    def _log_update(self, url: str, success: bool, error: str = "") -> None:
        """记录更新日志"""
        try:
            self.update_log.parent.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "成功" if success else "失败"
            log_entry = f"[{timestamp}] 订阅更新{status}: {url}"
            
            if not success and error:
                log_entry += f" - 错误: {error}"
            
            with open(self.update_log, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
                
        except Exception:
            pass  # 日志记录失败不影响主流程
    
    def get_update_log(self, lines: int = 20) -> List[str]:
        """获取更新日志"""
        try:
            if not self.update_log.exists():
                return []
            
            with open(self.update_log, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            return [line.strip() for line in all_lines[-lines:]]
            
        except Exception as e:
            raise ConfigError(f"读取更新日志失败: {e}")
    
    def get_current_subscription_url(self) -> Optional[str]:
        """获取当前订阅链接"""
        try:
            if self.config_url_file.exists():
                with open(self.config_url_file, 'r') as f:
                    return f.read().strip()
            return None
        except Exception:
            return None
