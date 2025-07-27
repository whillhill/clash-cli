"""
clash-cli 工具函数
"""

import os
import sys
import platform
import subprocess
import shutil
import gzip
import tarfile
import zipfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import psutil
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .constants import USER_AGENT, DOWNLOAD_TIMEOUT, REQUEST_TIMEOUT
from .exceptions import ClashCliError, PermissionError, NetworkError

console = Console()


def is_root() -> bool:
    """检查是否为 root 用户"""
    return os.geteuid() == 0


def check_root_permission() -> None:
    """检查 root 权限"""
    if not is_root():
        raise PermissionError("需要 root 权限执行此操作")


def get_system_info() -> Dict[str, str]:
    """获取系统信息"""
    try:
        # 获取发行版信息
        with open("/etc/os-release", "r") as f:
            os_release = f.read()
        
        distro = "unknown"
        version = "unknown"
        
        for line in os_release.split("\n"):
            if line.startswith("ID="):
                distro = line.split("=")[1].strip('"')
            elif line.startswith("VERSION_ID="):
                version = line.split("=")[1].strip('"')
        
        return {
            "distro": distro,
            "version": version,
            "arch": platform.machine(),
            "kernel": platform.release(),
            "python": platform.python_version(),
        }
    except Exception as e:
        raise ClashCliError(f"获取系统信息失败: {e}")


def get_architecture() -> str:
    """获取系统架构"""
    arch = platform.machine().lower()
    arch_map = {
        "x86_64": "x86_64",
        "amd64": "x86_64", 
        "aarch64": "aarch64",
        "arm64": "aarch64",
        "armv7l": "armv7",
        "armv7": "armv7",
    }
    return arch_map.get(arch, arch)


def check_systemd() -> bool:
    """检查是否支持 systemd"""
    try:
        result = subprocess.run(
            ["systemctl", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def run_command(
    cmd: List[str], 
    check: bool = True,
    capture_output: bool = True,
    timeout: Optional[int] = None,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None
) -> subprocess.CompletedProcess:
    """执行系统命令"""
    try:
        return subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=env
        )
    except subprocess.CalledProcessError as e:
        raise ClashCliError(f"命令执行失败: {' '.join(cmd)}\n错误: {e.stderr}")
    except subprocess.TimeoutExpired:
        raise ClashCliError(f"命令执行超时: {' '.join(cmd)}")
    except FileNotFoundError:
        raise ClashCliError(f"命令不存在: {cmd[0]}")


def is_port_in_use(port: int) -> bool:
    """检查端口是否被占用"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False


def find_free_port(start_port: int = 8000, end_port: int = 9000) -> int:
    """查找可用端口"""
    for port in range(start_port, end_port):
        if not is_port_in_use(port):
            return port
    raise ClashCliError(f"在 {start_port}-{end_port} 范围内未找到可用端口")


def download_file(
    url: str, 
    dest: Path, 
    show_progress: bool = True,
    headers: Optional[Dict[str, str]] = None
) -> None:
    """下载文件"""
    if headers is None:
        headers = {"User-Agent": USER_AGENT}
    
    try:
        with requests.get(url, headers=headers, stream=True, timeout=DOWNLOAD_TIMEOUT) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            if show_progress and total_size > 0:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"下载 {dest.name}", total=total_size)
                    
                    with open(dest, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                progress.update(task, advance=len(chunk))
            else:
                with open(dest, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
    except requests.RequestException as e:
        raise NetworkError(f"下载失败 {url}: {e}")


def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """解压文件"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    if archive_path.suffix == '.gz':
        if archive_path.name.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(dest_dir)
        else:
            # 单个 .gz 文件
            with gzip.open(archive_path, 'rb') as gz_file:
                output_file = dest_dir / archive_path.stem
                with open(output_file, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
                # 设置执行权限
                output_file.chmod(0o755)
    elif archive_path.suffix in ['.tar', '.tgz']:
        with tarfile.open(archive_path, 'r') as tar:
            tar.extractall(dest_dir)
    elif archive_path.suffix in ['.zip']:
        with zipfile.ZipFile(archive_path, 'r') as zip_file:
            zip_file.extractall(dest_dir)
    elif archive_path.suffix == '.xz':
        import lzma
        if archive_path.name.endswith('.tar.xz'):
            with lzma.open(archive_path, 'rb') as xz_file:
                with tarfile.open(fileobj=xz_file, mode='r') as tar:
                    tar.extractall(dest_dir)
        else:
            with lzma.open(archive_path, 'rb') as xz_file:
                output_file = dest_dir / archive_path.stem
                with open(output_file, 'wb') as out_file:
                    shutil.copyfileobj(xz_file, out_file)
    else:
        raise ClashCliError(f"不支持的压缩格式: {archive_path.suffix}")


def validate_url(url: str) -> bool:
    """验证 URL 格式"""
    try:
        response = requests.head(url, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_shell_type() -> str:
    """获取当前 shell 类型"""
    shell = os.environ.get('SHELL', '/bin/bash')
    if 'bash' in shell:
        return 'bash'
    elif 'zsh' in shell:
        return 'zsh'
    elif 'fish' in shell:
        return 'fish'
    else:
        return 'bash'  # 默认


def format_bytes(bytes_count: int) -> str:
    """格式化字节数"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"


def success_message(message: str) -> None:
    """显示成功消息"""
    console.print(f"😼 {message}", style="green")


def error_message(message: str) -> None:
    """显示错误消息"""
    console.print(f"😾 {message}", style="red")


def info_message(message: str) -> None:
    """显示信息消息"""
    console.print(f"ℹ️  {message}", style="blue")


def warning_message(message: str) -> None:
    """显示警告消息"""
    console.print(f"⚠️  {message}", style="yellow")
