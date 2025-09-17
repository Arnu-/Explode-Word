#!/usr/bin/env python3
"""
数据库配置测试脚本
用于验证 SQLite 和 MySQL 配置是否正常
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_sqlite_config():
    """测试 SQLite 配置"""
    print("=" * 50)
    print("测试 SQLite 配置")
    print("=" * 50)
    
    # 设置 SQLite 配置
    os.environ['DATABASE_TYPE'] = 'sqlite'
    
    try:
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            # 获取数据库 URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"数据库 URI: {db_uri}")
            
            # 测试数据库连接
            db.create_all()
            print("✅ SQLite 数据库连接成功")
            
            # 测试基本操作
            result = db.session.execute(db.text("SELECT 1")).scalar()
            if result == 1:
                print("✅ SQLite 数据库操作正常")
            else:
                print("❌ SQLite 数据库操作异常")
                
            return True
            
    except Exception as e:
        print(f"❌ SQLite 配置错误: {e}")
        return False


def test_mysql_config():
    """测试 MySQL 配置"""
    print("=" * 50)
    print("测试 MySQL 配置")
    print("=" * 50)
    
    # 检查 MySQL 配置
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_username = os.environ.get('MYSQL_USERNAME', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_database = os.environ.get('MYSQL_DATABASE', 'explode_word')
    
    print(f"MySQL 主机: {mysql_host}:{mysql_port}")
    print(f"MySQL 用户: {mysql_username}")
    print(f"MySQL 数据库: {mysql_database}")
    
    if not mysql_password:
        print("⚠️  警告: MySQL 密码为空")
    
    # 设置 MySQL 配置
    os.environ['DATABASE_TYPE'] = 'mysql'
    
    try:
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            # 获取数据库 URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            # 隐藏密码显示
            safe_uri = db_uri.replace(f':{mysql_password}@', ':***@') if mysql_password else db_uri
            print(f"数据库 URI: {safe_uri}")
            
            # 测试数据库连接
            db.create_all()
            print("✅ MySQL 数据库连接成功")
            
            # 测试基本操作
            result = db.session.execute(db.text("SELECT 1")).scalar()
            if result == 1:
                print("✅ MySQL 数据库操作正常")
            else:
                print("❌ MySQL 数据库操作异常")
                
            return True
            
    except Exception as e:
        print(f"❌ MySQL 配置错误: {e}")
        print("请检查:")
        print("1. MySQL 服务是否启动")
        print("2. 数据库是否存在")
        print("3. 用户名和密码是否正确")
        print("4. 是否安装了 PyMySQL 依赖")
        return False


def test_config_switching():
    """测试配置切换"""
    print("=" * 50)
    print("测试数据库配置切换")
    print("=" * 50)
    
    # 测试 SQLite
    sqlite_ok = test_sqlite_config()
    
    # 测试 MySQL（如果配置了的话）
    mysql_ok = False
    if os.environ.get('MYSQL_PASSWORD'):
        mysql_ok = test_mysql_config()
    else:
        print("跳过 MySQL 测试（未配置密码）")
    
    print("=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    print(f"SQLite 配置: {'✅ 正常' if sqlite_ok else '❌ 异常'}")
    print(f"MySQL 配置: {'✅ 正常' if mysql_ok else '❌ 异常或未配置'}")
    
    if sqlite_ok:
        print("\n✅ 项目可以正常使用 SQLite 数据库")
    
    if mysql_ok:
        print("✅ 项目可以正常使用 MySQL 数据库")
    elif os.environ.get('MYSQL_PASSWORD'):
        print("❌ MySQL 配置有问题，请检查配置")
    else:
        print("ℹ️  如需使用 MySQL，请在 .env 文件中配置相关参数")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == 'sqlite':
            test_sqlite_config()
        elif test_type == 'mysql':
            test_mysql_config()
        else:
            print("用法: python test_db_config.py [sqlite|mysql]")
    else:
        test_config_switching()