"""
clash-cli 异常类定义
"""


class ClashCliError(Exception):
    """clash-cli 基础异常类"""
    
    def __init__(self, message: str, code: int = 1):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ServiceError(ClashCliError):
    """服务相关异常"""
    pass


class ConfigError(ClashCliError):
    """配置相关异常"""
    pass


class NetworkError(ClashCliError):
    """网络相关异常"""
    pass


class PermissionError(ClashCliError):
    """权限相关异常"""
    pass


class InstallationError(ClashCliError):
    """安装相关异常"""
    pass


class ValidationError(ClashCliError):
    """验证相关异常"""
    pass
