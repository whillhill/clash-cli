"""
clash-cli: Linux 一键安装 Clash 代理工具

一个简单易用的 Linux Clash 代理工具，支持一键安装、配置和管理。
"""

__version__ = "1.0.1"
__author__ = "whillhill"
__email__ = "ooooofish@126.com"
__license__ = "MIT"
__url__ = "https://github.com/whillhill/clash-cli"

from .core.service import ClashService
from .core.config import ClashConfig
from .core.proxy import ProxyManager
from .exceptions import ClashCliError, ServiceError, ConfigError

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__url__",
    "ClashService",
    "ClashConfig", 
    "ProxyManager",
    "ClashCliError",
    "ServiceError",
    "ConfigError",
]
