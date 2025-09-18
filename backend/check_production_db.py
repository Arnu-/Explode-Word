#!/usr/bin/env python3
"""
检查生产环境Flask应用使用的数据库配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from app import create_app

def check_production_database_config():
    """检查生产环境数据库配置"""
    print("=== 生产环境Flask应用数据库配置检查 ===\n")
    
    # 先清除现有环境变量，然后加载生产环境变量
    import importlib
    import config.config
    
    # 加载生产环境变量
    load_dotenv('.env.production', override=True)
    
    # 重新加载配置模块以使用新的环境变量
    importlib.reload(config.config)
    
    # 创建生产环境应用实例
    app = create_app('production')
    
    with app.app_context():
        # 获取数据库URI
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"数据库URI: {db_uri}")
        
        # 解析SQLite数据库文件路径
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(db_path):
                backend_dir = Path(__file__).parent.absolute()
                db_path = backend_dir / db_path
            
            print(f"SQLite数据库文件路径: {db_path}")
            print(f"数据库文件是否存在: {'是' if os.path.exists(db_path) else '否'}")
            
            if os.path.exists(db_path):
                # 获取文件大小
                file_size = os.path.getsize(db_path)
                print(f"数据库文件大小: {file_size} 字节 ({file_size/1024:.2f} KB)")
                
                # 获取文件修改时间
                import datetime
                mtime = os.path.getmtime(db_path)
                mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"最后修改时间: {mtime_str}")
        
        # 显示其他相关配置
        print(f"\n其他配置信息:")
        print(f"DEBUG模式: {app.config.get('DEBUG', False)}")
        print(f"环境: {os.environ.get('FLASK_ENV', 'production')}")
        print(f"数据库类型配置: {os.environ.get('DATABASE_TYPE', 'sqlite')}")
        print(f"SQLite路径配置: {os.environ.get('SQLITE_DB_PATH', 'explode_word.db')}")
        print(f"服务器HOST: {os.environ.get('HOST', '0.0.0.0')}")
        print(f"服务器PORT: {os.environ.get('PORT', '8000')}")

if __name__ == '__main__':
    check_production_database_config()