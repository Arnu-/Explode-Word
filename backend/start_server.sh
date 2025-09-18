#!/bin/bash

# Explode Word Backend 启动脚本

# 设置环境变量
export FLASK_ENV=production
export PORT=${PORT:-8000}

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "已激活虚拟环境"
fi

# 检查依赖
echo "检查依赖..."
pip install -r requirements.txt

# SQLite 数据库初始化
echo "初始化 SQLite 数据库..."
python -c "
from app import create_app, db
import os

# 确保数据库目录存在
os.makedirs('data', exist_ok=True)

app = create_app('production')
with app.app_context():
    db.create_all()
    print('SQLite 数据库初始化完成')
    print(f'数据库文件位置: {app.config[\"SQLALCHEMY_DATABASE_URI\"]}')
"

# 启动 Gunicorn
echo "启动 Gunicorn 服务器..."
gunicorn --config gunicorn.conf.py wsgi:application