#!/usr/bin/env python3
"""
数据库状态检查脚本
"""
import os
from pathlib import Path
from app import create_app, db

def check_database_status():
    """检查数据库状态"""
    app = create_app('production')
    
    with app.app_context():
        # 获取数据库 URI
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"数据库 URI: {db_uri}")
        
        # 检查 SQLite 文件是否存在
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            db_file = Path(db_path)
            
            if db_file.exists():
                file_size = db_file.stat().st_size
                print(f"✅ SQLite 数据库文件存在")
                print(f"📁 文件路径: {db_file.absolute()}")
                print(f"📊 文件大小: {file_size} bytes ({file_size/1024:.2f} KB)")
            else:
                print(f"❌ SQLite 数据库文件不存在: {db_file.absolute()}")
                print("💡 运行以下命令创建数据库:")
                print("   python init_db.py")
                return False
        
        # 检查数据库连接
        try:
            # 尝试连接数据库
            with db.engine.connect() as conn:
                conn.execute(db.text('SELECT 1'))
            print("✅ 数据库连接正常")
            
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 数据库表 ({len(tables)} 个):")
                for table in sorted(tables):
                    print(f"   - {table}")
            else:
                print("⚠️  数据库中没有表")
                print("💡 运行以下命令创建表:")
                print("   python -c \"from app import create_app, db; app=create_app('production'); app.app_context().push(); db.create_all()\"")
            
            return True
            
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False

if __name__ == '__main__':
    print("🔍 检查数据库状态...")
    print("=" * 50)
    
    success = check_database_status()
    
    print("=" * 50)
    if success:
        print("✅ 数据库检查完成")
    else:
        print("❌ 数据库检查发现问题")
        exit(1)