#!/bin/bash

# Explode Word 游戏系统启动脚本
# 用于快速启动整个游戏系统（后端 + 前端）

set -e  # 遇到错误立即退出

echo "🎮 Explode Word 游戏系统启动脚本"
echo "=================================="

# 检查是否在项目根目录
if [ ! -f "GAME_RECORDS_README.md" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 函数：检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查必要的命令
echo "🔍 检查系统依赖..."
check_command python3
check_command npm
check_command node

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x backend/scripts/*.py
chmod +x start_game_system.sh

# 后端设置
echo ""
echo "🐍 设置后端环境..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装后端依赖..."
pip install -r requirements.txt 2>/dev/null || echo "⚠️  requirements.txt 不存在，请手动安装依赖"

# 初始化数据库
echo "🗄️  初始化数据库..."
export FLASK_APP=app
flask db init 2>/dev/null || echo "数据库已初始化"
flask db migrate -m "Initial migration" 2>/dev/null || echo "迁移文件已存在"
flask db upgrade 2>/dev/null || echo "数据库已是最新版本"

# 初始化游戏数据
echo "🎯 初始化游戏数据..."
python scripts/setup_game_data.py

# 启动后端服务
echo "🚀 启动后端服务..."
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000 &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 前端设置
echo ""
echo "🌐 设置前端环境..."
cd ../frontend

# 安装依赖
echo "📥 安装前端依赖..."
npm install

# 启动前端服务
echo "🚀 启动前端服务..."
npm run dev &
FRONTEND_PID=$!

# 等待前端启动
echo "⏳ 等待前端服务启动..."
sleep 5

echo ""
echo "✅ 游戏系统启动完成！"
echo "=================================="
echo "🌐 前端地址: http://localhost:5173"
echo "🐍 后端地址: http://localhost:5000"
echo "👤 测试账号: demo / demo123"
echo ""
echo "📋 可用的关卡："
echo "   1. 魔法森林挑战 (简单)"
echo "   2. 水晶洞穴探险 (简单)"
echo "   3. 古老遗迹挑战 (中等)"
echo "   4. 火山熔岩试炼 (中等)"
echo "   5. 冰雪王国征服 (中等)"
echo "   6. 暗影深渊挑战 (困难)"
echo "   7. 龙族圣地 (困难)"
echo "   8. 终极试炼 (地狱)"
echo ""
echo "🛑 按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ 所有服务已停止'; exit 0" INT

# 保持脚本运行
wait