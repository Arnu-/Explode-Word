# 🚀 Explode Word 游戏记录系统 - 快速启动指南

## 📋 系统要求

- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 8+
- **操作系统**: macOS/Linux/Windows

## ⚡ 一键启动（推荐）

```bash
# 1. 进入项目根目录
cd /path/to/Explode-Word

# 2. 运行启动脚本
./start_game_system.sh
```

启动脚本会自动：
- ✅ 检查系统依赖
- ✅ 设置Python虚拟环境
- ✅ 安装后端依赖
- ✅ 初始化数据库
- ✅ 创建示例数据
- ✅ 启动后端服务 (端口5000)
- ✅ 安装前端依赖
- ✅ 启动前端服务 (端口5173)

## 🎯 访问系统

启动完成后：

### 前端界面
- **地址**: http://localhost:5173
- **测试账号**: demo / demo123

### 后端API
- **地址**: http://localhost:5000
- **API文档**: http://localhost:5000/api

## 🎮 功能测试

### 1. 登录系统
```
用户名: demo
密码: demo123
```

### 2. 查看关卡
- 进入关卡选择页面
- 查看8个示例关卡
- 前3个关卡有游戏记录

### 3. 测试功能
- **关卡状态**: 已完成/可用/锁定
- **星级显示**: 0-3星评价
- **任务系统**: 查看任务完成状态
- **进度统计**: 游戏进度和成就进度

## 🛠️ 手动启动（高级用户）

### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（如果不存在）
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 4. 安装依赖
pip install flask flask-sqlalchemy flask-migrate flask-cors flask-jwt-extended

# 5. 初始化数据库
export FLASK_APP=app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 6. 初始化游戏数据
python scripts/setup_game_data.py

# 7. 启动服务
flask run --host=0.0.0.0 --port=5000
```

### 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

## 🧪 系统测试

### 运行测试脚本
```bash
cd backend
python scripts/test_game_records.py
```

### 测试API接口
```bash
# 测试关卡列表（需要认证）
curl -X GET "http://localhost:5000/api/levels/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 测试用户进度
curl -X GET "http://localhost:5000/api/levels/progress" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📊 数据管理

### 重置游戏数据
```bash
cd backend
rm instance/app.db  # 删除数据库文件
python scripts/setup_game_data.py  # 重新初始化
```

### 创建新用户
```bash
cd backend
python scripts/create_demo_user.py
```

### 添加关卡数据
```bash
cd backend
python scripts/init_levels.py
```

## 🔧 配置说明

### 环境变量
```bash
# 后端配置
export FLASK_ENV=development
export FLASK_DEBUG=1
export DATABASE_URL=sqlite:///app.db

# 前端配置（在 frontend/src/config/env.js）
API_BASE_URL=/api  # 开发环境使用代理
```

### 数据库配置
```python
# config/config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # 开发环境
# SQLALCHEMY_DATABASE_URI = 'postgresql://...'  # 生产环境
```

## 🚨 常见问题

### 1. 端口被占用
```bash
# 查看端口占用
lsof -i :5000  # 后端端口
lsof -i :5173  # 前端端口

# 杀死进程
kill -9 PID
```

### 2. Python虚拟环境问题
```bash
# 删除虚拟环境重新创建
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. 数据库迁移错误
```bash
cd backend
rm -rf migrations/  # 删除迁移文件
rm instance/app.db  # 删除数据库
flask db init       # 重新初始化
```

### 4. 前端依赖安装失败
```bash
cd frontend
rm -rf node_modules/
rm package-lock.json
npm install
```

## 📱 移动端适配

系统支持响应式设计：
- **桌面端**: 3x3关卡网格
- **平板端**: 2x2关卡网格  
- **手机端**: 1列关卡列表

## 🔒 安全说明

### 开发环境
- JWT密钥使用默认值
- 数据库无密码保护
- CORS允许所有来源

### 生产环境建议
- 设置强JWT密钥
- 配置数据库密码
- 限制CORS来源
- 启用HTTPS

## 📈 性能监控

### 后端性能
```bash
# 查看API响应时间
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:5000/api/levels/
```

### 前端性能
- 打开浏览器开发者工具
- 查看Network面板
- 监控API调用时间

## 🎯 下一步

1. **体验功能**: 登录系统，体验关卡选择和记录功能
2. **查看代码**: 了解实现细节和架构设计
3. **扩展功能**: 基于现有系统添加新功能
4. **部署上线**: 配置生产环境并部署

## 📞 获取帮助

### 查看日志
```bash
# 后端日志
tail -f backend/logs/app.log

# 前端控制台
# 打开浏览器开发者工具查看Console
```

### 系统状态检查
```bash
# 检查后端服务
curl http://localhost:5000/api/health

# 检查数据库
cd backend && python -c "from app import create_app, db; app=create_app(); app.app_context().push(); print('DB OK' if db.engine.execute('SELECT 1').scalar() == 1 else 'DB Error')"
```

---

🎉 **恭喜！** 您已成功启动 Explode Word 游戏记录系统！

现在可以开始体验完整的游戏记录功能了。如有问题，请查看详细文档 `GAME_RECORDS_README.md`。