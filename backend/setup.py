#!/usr/bin/env python3
"""
项目快速设置脚本
"""
import os
import sys
import subprocess
from pathlib import Path


def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    try:
        _ = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                          check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def create_env_file():
    """创建环境配置文件"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("⚠️  .env 文件已存在，跳过创建")
        return True
    
    if not env_example.exists():
        print("❌ .env.example 文件不存在")
        return False
    
    try:
        # 复制示例文件
        with open(env_example, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已创建 .env 配置文件")
        print("ℹ️  请根据需要编辑 .env 文件中的配置")
        return True
        
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")
        return False


def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    try:
        subprocess.run([sys.executable, 'init_db.py'], check=True)
        print("✅ 数据库初始化完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False


def test_configuration():
    """测试配置"""
    print("正在测试配置...")
    try:
        subprocess.run([sys.executable, 'test_db_config.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 配置测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("Explode Word 后端项目快速设置")
    print("=" * 60)
    
    # 检查 Python 版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        sys.exit(1)
    
    print(f"✅ Python 版本: {sys.version}")
    
    # 步骤1: 安装依赖
    if not install_dependencies():
        print("设置失败，请检查依赖安装")
        sys.exit(1)
    
    # 步骤2: 创建环境配置文件
    if not create_env_file():
        print("设置失败，请检查环境配置文件")
        sys.exit(1)
    
    # 步骤3: 初始化数据库
    if not init_database():
        print("设置失败，请检查数据库配置")
        sys.exit(1)
    
    # 步骤4: 测试配置
    print("\n" + "=" * 60)
    print("测试项目配置")
    print("=" * 60)
    test_configuration()
    
    print("\n" + "=" * 60)
    print("设置完成！")
    print("=" * 60)
    print("现在可以启动项目:")
    print("  python run.py")
    print("")
    print("或者使用 Flask 命令:")
    print("  export FLASK_APP=run.py")
    print("  flask run")
    print("")
    print("API 文档: http://127.0.0.1:5000")
    print("=" * 60)


if __name__ == '__main__':
    main()