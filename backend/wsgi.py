"""
WSGI 入口文件
用于 Gunicorn 等 WSGI 服务器
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app

# 加载环境变量
load_dotenv()

# 获取配置环境
config_name = os.environ.get('FLASK_ENV', 'production')

# 创建应用实例
application = create_app(config_name)

if __name__ == "__main__":
    application.run()