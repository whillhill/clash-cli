"""
Clash 服务管理
"""

import time
from pathlib import Path
from typing import Optional, Dict, Any

from ..constants import (
    SERVICE_NAME, SYSTEMD_SERVICE_FILE, CLASH_BASE_DIR, 
    CLASH_CONFIG_RUNTIME, BIN_MIHOMO, SERVICE_TIMEOUT
)
from ..exceptions import ServiceError, PermissionError
from ..utils import (
    check_root_permission, run_command, success_message, 
    error_message, info_message
)


class ClashService:
    """Clash 服务管理器"""
    
    def __init__(self):
        self.service_name = SERVICE_NAME
        self.service_file = SYSTEMD_SERVICE_FILE
        
    def is_installed(self) -> bool:
        """检查服务是否已安装"""
        return self.service_file.exists()
    
    def is_running(self) -> bool:
        """检查服务是否正在运行"""
        try:
            result = run_command(
                ["systemctl", "is-active", self.service_name],
                check=False,
                timeout=5
            )
            return result.returncode == 0 and result.stdout.strip() == "active"
        except Exception:
            return False
    
    def is_enabled(self) -> bool:
        """检查服务是否已启用（开机自启）"""
        try:
            result = run_command(
                ["systemctl", "is-enabled", self.service_name],
                check=False,
                timeout=5
            )
            return result.returncode == 0 and result.stdout.strip() == "enabled"
        except Exception:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        try:
            result = run_command(
                ["systemctl", "status", self.service_name, "--no-pager"],
                check=False,
                timeout=10
            )
            
            return {
                "installed": self.is_installed(),
                "running": self.is_running(),
                "enabled": self.is_enabled(),
                "status_output": result.stdout,
                "exit_code": result.returncode
            }
        except Exception as e:
            return {
                "installed": self.is_installed(),
                "running": False,
                "enabled": False,
                "status_output": f"获取状态失败: {e}",
                "exit_code": 1
            }
    
    def install_service(self) -> None:
        """安装 systemd 服务"""
        check_root_permission()
        
        if not BIN_MIHOMO.exists():
            raise ServiceError("Mihomo 二进制文件不存在，请先安装")
        
        if not CLASH_CONFIG_RUNTIME.exists():
            raise ServiceError("配置文件不存在，请先配置")
        
        service_content = f"""[Unit]
Description=mihomo Daemon, A[nother] Clash Kernel.
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=5
User=root
ExecStart={BIN_MIHOMO} -d {CLASH_BASE_DIR} -f {CLASH_CONFIG_RUNTIME}
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open(self.service_file, 'w') as f:
                f.write(service_content)
            
            # 重新加载 systemd
            run_command(["systemctl", "daemon-reload"], timeout=10)
            success_message("服务安装成功")
            
        except Exception as e:
            raise ServiceError(f"安装服务失败: {e}")
    
    def uninstall_service(self) -> None:
        """卸载 systemd 服务"""
        check_root_permission()
        
        try:
            # 停止服务
            if self.is_running():
                self.stop()
            
            # 禁用服务
            if self.is_enabled():
                self.disable()
            
            # 删除服务文件
            if self.service_file.exists():
                self.service_file.unlink()
            
            # 重新加载 systemd
            run_command(["systemctl", "daemon-reload"], timeout=10)
            success_message("服务卸载成功")
            
        except Exception as e:
            raise ServiceError(f"卸载服务失败: {e}")
    
    def start(self) -> None:
        """启动服务"""
        check_root_permission()
        
        if not self.is_installed():
            raise ServiceError("服务未安装，请先安装")
        
        try:
            if self.is_running():
                info_message("服务已在运行")
                return
            
            run_command(["systemctl", "start", self.service_name], timeout=SERVICE_TIMEOUT)
            
            # 等待服务启动
            for _ in range(10):
                if self.is_running():
                    success_message("服务启动成功")
                    return
                time.sleep(1)
            
            raise ServiceError("服务启动超时")
            
        except Exception as e:
            raise ServiceError(f"启动服务失败: {e}")
    
    def stop(self) -> None:
        """停止服务"""
        check_root_permission()
        
        try:
            if not self.is_running():
                info_message("服务未运行")
                return
            
            run_command(["systemctl", "stop", self.service_name], timeout=SERVICE_TIMEOUT)
            
            # 等待服务停止
            for _ in range(10):
                if not self.is_running():
                    success_message("服务停止成功")
                    return
                time.sleep(1)
            
            raise ServiceError("服务停止超时")
            
        except Exception as e:
            raise ServiceError(f"停止服务失败: {e}")
    
    def restart(self) -> None:
        """重启服务"""
        check_root_permission()
        
        try:
            run_command(["systemctl", "restart", self.service_name], timeout=SERVICE_TIMEOUT)
            
            # 等待服务重启
            for _ in range(15):
                if self.is_running():
                    success_message("服务重启成功")
                    return
                time.sleep(1)
            
            raise ServiceError("服务重启超时")
            
        except Exception as e:
            raise ServiceError(f"重启服务失败: {e}")
    
    def enable(self) -> None:
        """启用服务（开机自启）"""
        check_root_permission()
        
        if not self.is_installed():
            raise ServiceError("服务未安装，请先安装")
        
        try:
            if self.is_enabled():
                info_message("服务已启用开机自启")
                return
            
            run_command(["systemctl", "enable", self.service_name], timeout=10)
            success_message("已启用开机自启")
            
        except Exception as e:
            raise ServiceError(f"启用服务失败: {e}")
    
    def disable(self) -> None:
        """禁用服务（取消开机自启）"""
        check_root_permission()
        
        try:
            if not self.is_enabled():
                info_message("服务未启用开机自启")
                return
            
            run_command(["systemctl", "disable", self.service_name], timeout=10)
            success_message("已禁用开机自启")
            
        except Exception as e:
            raise ServiceError(f"禁用服务失败: {e}")
    
    def get_logs(self, lines: int = 50, follow: bool = False) -> str:
        """获取服务日志"""
        try:
            cmd = ["journalctl", "-u", self.service_name, "--no-pager"]
            
            if lines > 0:
                cmd.extend(["-n", str(lines)])
            
            if follow:
                cmd.append("-f")
            
            result = run_command(cmd, timeout=10 if not follow else None)
            return result.stdout
            
        except Exception as e:
            raise ServiceError(f"获取日志失败: {e}")

    def reload_config(self) -> None:
        """重新加载配置"""
        check_root_permission()

        if not self.is_running():
            raise ServiceError("服务未运行，无法重新加载配置")

        try:
            run_command(["systemctl", "reload", self.service_name], timeout=10)
            success_message("配置重新加载成功")
        except Exception as e:
            # 如果 reload 失败，尝试 restart
            try:
                self.restart()
            except Exception:
                raise ServiceError(f"重新加载配置失败: {e}")
