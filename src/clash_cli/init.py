"""
clash-cli 初始化器

负责将打包的脚本和资源文件部署到系统，并提供使用指导。
"""

import os
import shutil
import stat
import subprocess
from pathlib import Path
from typing import Optional
import click
import pkg_resources


class ClashInitializer:
    """Clash 初始化器"""

    def __init__(self, mode: str = 'init', target_dir: str = '/tmp/clash-cli',
                 force: bool = False, subscription: Optional[str] = None):
        self.mode = mode  # 'init', 'install', 'uninstall'
        self.target_dir = Path(target_dir)
        self.force = force
        self.subscription = subscription
        self.package_name = 'clash_cli'

        # 根据模式设置目标目录
        if mode in ['install', 'uninstall']:
            self.target_dir = Path('/tmp/clash-cli-temp')
            self.force = True  # 临时目录总是强制覆盖
    
    def run(self):
        """运行初始化流程"""
        if self.mode == 'install':
            self._run_install()
        elif self.mode == 'uninstall':
            self._run_uninstall()
        else:  # init mode
            self._run_init()

    def _run_install(self):
        """运行安装流程"""
        click.echo("🚀 开始安装 Clash...")

        # 1. 检查环境
        self._check_environment()

        # 2. 准备临时目录
        self._prepare_target_directory()

        # 3. 提取脚本和资源文件
        self._extract_resources()

        # 4. 设置权限
        self._set_permissions()

        # 5. 执行安装脚本
        self._execute_install_script()

        # 6. 清理临时文件
        self._cleanup_temp_directory()

        click.echo("✅ Clash 安装完成！")

    def _run_uninstall(self):
        """运行卸载流程"""
        click.echo("🗑️  开始卸载 Clash...")

        # 1. 检查环境
        self._check_environment()

        # 2. 准备临时目录
        self._prepare_target_directory()

        # 3. 提取脚本文件
        self._extract_resources()

        # 4. 设置权限
        self._set_permissions()

        # 5. 执行卸载脚本
        self._execute_uninstall_script()

        # 6. 清理临时文件
        self._cleanup_temp_directory()

        click.echo("✅ Clash 卸载完成！")

    def _run_init(self):
        """运行初始化流程"""
        click.echo("🚀 开始初始化 Clash 环境...")

        # 1. 检查环境
        self._check_environment()

        # 2. 准备目标目录
        self._prepare_target_directory()

        # 3. 提取脚本和资源文件
        self._extract_resources()

        # 4. 设置权限
        self._set_permissions()

        # 5. 显示使用指导
        self._show_usage_guide()

        click.echo("✅ 初始化完成！")
    
    def _check_environment(self):
        """检查环境"""
        click.echo("🔍 检查系统环境...")
        
        # 检查 systemd
        if not Path('/bin/systemctl').exists() and not Path('/usr/bin/systemctl').exists():
            raise RuntimeError("系统不支持 systemd")
        
        # 检查必要命令
        required_commands = ['bash', 'curl', 'tar', 'gzip']
        missing_commands = []
        
        for cmd in required_commands:
            if not shutil.which(cmd):
                missing_commands.append(cmd)
        
        if missing_commands:
            raise RuntimeError(f"缺少必要命令: {', '.join(missing_commands)}")
        
        click.echo("✅ 环境检查通过")
    
    def _prepare_target_directory(self):
        """准备目标目录"""
        click.echo(f"📁 准备目标目录: {self.target_dir}")
        
        if self.target_dir.exists():
            if not self.force:
                if not click.confirm(f"目录 {self.target_dir} 已存在，是否覆盖？"):
                    raise RuntimeError("用户取消操作")
            
            click.echo("🗑️  清理已存在的目录...")
            shutil.rmtree(self.target_dir)
        
        self.target_dir.mkdir(parents=True, exist_ok=True)
        click.echo("✅ 目录准备完成")
    
    def _extract_resources(self):
        """提取脚本和资源文件"""
        click.echo("📦 提取脚本和资源文件...")
        
        # 获取包资源路径
        try:
            # 提取根目录的脚本文件
            root_scripts = ['install.sh', 'uninstall.sh']
            for script in root_scripts:
                if pkg_resources.resource_exists(self.package_name, f'resources/{script}'):
                    content = pkg_resources.resource_string(self.package_name, f'resources/{script}')
                    target_file = self.target_dir / script
                    target_file.write_bytes(content)
                    click.echo(f"  ✓ {script}")

            # 提取 script 目录
            script_dir = self.target_dir / 'script'
            script_dir.mkdir(exist_ok=True)

            script_files = ['common.sh', 'clash-cli.sh', 'clash-cli.fish']
            for script_file in script_files:
                resource_path = f'resources/script/{script_file}'
                if pkg_resources.resource_exists(self.package_name, resource_path):
                    content = pkg_resources.resource_string(self.package_name, resource_path)
                    target_file = script_dir / script_file
                    target_file.write_bytes(content)
                    click.echo(f"  ✓ script/{script_file}")

            # 提取 resources 目录
            resources_dir = self.target_dir / 'resources'
            resources_dir.mkdir(exist_ok=True)

            # 提取 mixin.yaml
            if pkg_resources.resource_exists(self.package_name, 'resources/resources/mixin.yaml'):
                content = pkg_resources.resource_string(self.package_name, 'resources/resources/mixin.yaml')
                (resources_dir / 'mixin.yaml').write_bytes(content)
                click.echo(f"  ✓ resources/mixin.yaml")

            # 提取其他资源文件
            self._extract_directory('resources/resources/zip', resources_dir / 'zip')
            self._extract_directory('resources/resources/fallback', resources_dir / 'fallback')

            # 提取 Country.mmdb 如果存在
            if pkg_resources.resource_exists(self.package_name, 'resources/resources/Country.mmdb'):
                content = pkg_resources.resource_string(self.package_name, 'resources/resources/Country.mmdb')
                (resources_dir / 'Country.mmdb').write_bytes(content)
                click.echo(f"  ✓ resources/Country.mmdb")

            # 提取 preview.png 如果存在
            if pkg_resources.resource_exists(self.package_name, 'resources/resources/preview.png'):
                content = pkg_resources.resource_string(self.package_name, 'resources/resources/preview.png')
                (resources_dir / 'preview.png').write_bytes(content)
                click.echo(f"  ✓ resources/preview.png")
                
        except Exception as e:
            raise RuntimeError(f"提取资源文件失败: {e}")
        
        click.echo("✅ 资源文件提取完成")
    
    def _extract_directory(self, resource_path: str, target_path: Path):
        """提取目录中的所有文件"""
        target_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # 尝试列出目录中的文件
            # 注意：pkg_resources 不直接支持列出目录，我们需要预知文件名
            # 这里我们根据你的实际文件结构来硬编码
            
            if 'zip' in resource_path:
                zip_files = [
                    'mihomo-linux-amd64-compatible-v1.19.2.gz',
                    'subconverter_linux64.tar.gz', 
                    'yacd.tar.xz',
                    'yq_linux_amd64.tar.gz'
                ]
                for file_name in zip_files:
                    full_path = f"{resource_path}/{file_name}"
                    if pkg_resources.resource_exists(self.package_name, full_path):
                        content = pkg_resources.resource_string(self.package_name, full_path)
                        (target_path / file_name).write_bytes(content)
                        click.echo(f"  ✓ {resource_path}/{file_name}")
            
            elif 'fallback' in resource_path:
                fallback_files = [
                    'mihomo-linux-amd64-v1.17.0.gz',
                    'versions.json',
                    'yq_linux_amd64.tar.gz'
                ]
                for file_name in fallback_files:
                    full_path = f"{resource_path}/{file_name}"
                    if pkg_resources.resource_exists(self.package_name, full_path):
                        content = pkg_resources.resource_string(self.package_name, full_path)
                        (target_path / file_name).write_bytes(content)
                        click.echo(f"  ✓ {resource_path}/{file_name}")
                        
        except Exception as e:
            # 如果提取失败，不是致命错误，继续执行
            click.echo(f"  ⚠️  提取 {resource_path} 时出现问题: {e}")
    
    def _set_permissions(self):
        """设置文件权限"""
        click.echo("🔐 设置文件权限...")
        
        # 设置脚本文件为可执行
        script_files = [
            self.target_dir / 'install.sh',
            self.target_dir / 'uninstall.sh',
            self.target_dir / 'script' / 'common.sh',
            self.target_dir / 'script' / 'clash-cli.sh',
            self.target_dir / 'script' / 'clash-cli.fish',
        ]
        
        for script_file in script_files:
            if script_file.exists():
                # 设置为可读可写可执行 (755)
                script_file.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                click.echo(f"  ✓ {script_file.name}")
        
        click.echo("✅ 权限设置完成")

    def _execute_install_script(self):
        """执行安装脚本"""
        click.echo("⚙️  执行安装脚本...")

        install_script = self.target_dir / 'install.sh'
        if not install_script.exists():
            raise RuntimeError("安装脚本不存在")

        # 构建命令
        cmd = ['bash', str(install_script)]

        # 如果有订阅链接，通过环境变量传递
        env = os.environ.copy()
        if self.subscription:
            env['CLASH_SUBSCRIPTION_URL'] = self.subscription

        try:
            # 切换到脚本目录执行
            result = subprocess.run(
                cmd,
                cwd=str(self.target_dir),
                env=env,
                check=True
            )
            click.echo("✅ 安装脚本执行完成")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"安装脚本执行失败: {e}")

    def _execute_uninstall_script(self):
        """执行卸载脚本"""
        click.echo("⚙️  执行卸载脚本...")

        uninstall_script = self.target_dir / 'uninstall.sh'
        if not uninstall_script.exists():
            raise RuntimeError("卸载脚本不存在")

        try:
            # 切换到脚本目录执行
            result = subprocess.run(
                ['bash', str(uninstall_script)],
                cwd=str(self.target_dir),
                check=True
            )
            click.echo("✅ 卸载脚本执行完成")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"卸载脚本执行失败: {e}")

    def _cleanup_temp_directory(self):
        """清理临时目录"""
        if self.mode in ['install', 'uninstall'] and self.target_dir.exists():
            click.echo("🧹 清理临时文件...")
            shutil.rmtree(self.target_dir)
            click.echo("✅ 临时文件清理完成")

    def _show_usage_guide(self):
        """显示使用指导"""
        click.echo("\n" + "="*60)
        click.echo("🎉 Clash 环境初始化完成！")
        click.echo("="*60)
        click.echo(f"\n📁 脚本已部署到: {self.target_dir}")
        click.echo("\n🚀 接下来的使用步骤:")
        click.echo(f"\n1. 进入脚本目录:")
        click.echo(f"   cd {self.target_dir}")
        click.echo(f"\n2. 安装 Clash (需要 root 权限):")
        click.echo(f"   sudo bash install.sh")
        click.echo(f"\n3. 使用 Clash 命令:")
        click.echo(f"   clash-cli on      # 开启代理")
        click.echo(f"   clash-cli off     # 关闭代理")
        click.echo(f"   clash-cli status  # 查看状态")
        click.echo(f"   clash-cli ui      # Web 控制台")
        click.echo(f"   clash-cli --help  # 查看帮助")
        click.echo(f"\n4. 卸载 (如需要):")
        click.echo(f"   sudo bash uninstall.sh")
        click.echo("\n💡 提示: 所有业务功能都由高效的 Shell 脚本处理")
        click.echo("="*60)
