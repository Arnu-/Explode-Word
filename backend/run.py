#!/usr/bin/env python3
"""
应用启动脚本
"""
import os
from dotenv import load_dotenv
from app import create_app

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 开发环境配置
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )