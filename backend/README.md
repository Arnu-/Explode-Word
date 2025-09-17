# Explode Word 后端项目

这是一个基于 Flask 的单词爆炸游戏后端项目，支持 SQLite（默认）和 MySQL 数据库。

## 功能特性

- 🎮 多人在线单词游戏
- 📚 单词分类管理
- 👥 用户认证和管理
- 🏆 游戏统计和排行榜
- 🔄 数据库类型切换（SQLite ↔ MySQL）
- 🚀 RESTful API 设计

## 数据库配置

### 默认配置（SQLite）

项目默认使用 SQLite 数据库，无需额外配置即可运行：

```bash
# 直接运行，使用默认 SQLite 配置
python run.py
```

### 切换到 MySQL

1. **安装 MySQL 依赖**：
   ```bash
   pip install PyMySQL cryptography
   ```

2. **创建环境配置文件**：
   ```bash
   cp .env.example .env
   ```

3. **编辑 `.env` 文件**：
   ```env
   # 数据库配置
   DATABASE_TYPE=mysql
   
   # MySQL 配置
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USERNAME=root
   MYSQL_PASSWORD=your-password
   MYSQL_DATABASE=explode_word
   ```

4. **创建 MySQL 数据库**：
   ```sql
   CREATE DATABASE explode_word CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置文件（可选，默认使用 SQLite）
vim .env
```

### 3. 初始化数据库

```bash
# 初始化数据库和示例数据
python init_db.py
```

### 4. 启动应用

```bash
# 开发模式启动
python run.py

# 或使用 Flask 命令
export FLASK_APP=run.py
flask run
```

应用将在 `http://127.0.0.1:5000` 启动。

## 数据库迁移

项目提供了便捷的数据库迁移工具，支持在 SQLite 和 MySQL 之间迁移数据：

### 导出当前数据库数据

```bash
python migrate_db.py export
```

### 导入数据到新数据库

```bash
python migrate_db.py import
```

### 完整迁移流程

```bash
# 从 SQLite 迁移到 MySQL
python migrate_db.py migrate sqlite mysql

# 从 MySQL 迁移到 SQLite
python migrate_db.py migrate mysql sqlite
```

## API 接口

### 认证接口

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/profile` - 获取用户信息

### 用户管理

- `GET /api/users/` - 获取用户列表
- `GET /api/users/{id}` - 获取用户详情

### 游戏配置

- `GET /api/games/` - 获取游戏配置列表
- `GET /api/games/{id}` - 获取游戏配置详情

### 单词管理

- `GET /api/words/categories` - 获取单词分类
- `GET /api/words/` - 获取单词列表

### 游戏会话

- `POST /api/game-sessions/` - 创建游戏会话
- `GET /api/game-sessions/{room_code}` - 获取游戏会话信息

## 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂
│   ├── api/               # API 蓝图
│   │   ├── __init__.py
│   │   ├── auth.py        # 认证接口
│   │   ├── users.py       # 用户管理
│   │   ├── games.py       # 游戏配置
│   │   ├── words.py       # 单词管理
│   │   └── game_sessions.py # 游戏会话
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py        # 用户模型
│   │   ├── game.py        # 游戏模型
│   │   └── word.py        # 单词模型
│   └── utils/             # 工具模块
│       ├── __init__.py
│       ├── error_handlers.py # 错误处理
│       └── validators.py  # 数据验证
├── config/                # 配置模块
│   ├── __init__.py
│   └── config.py          # 应用配置
├── tests/                 # 测试模块
├── .env.example           # 环境配置示例
├── init_db.py            # 数据库初始化
├── migrate_db.py         # 数据库迁移工具
├── run.py                # 应用启动脚本
├── requirements.txt      # 依赖包列表
└── README.md             # 项目说明
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_ENV` | Flask 环境 | `development` |
| `SECRET_KEY` | 应用密钥 | 自动生成 |
| `DATABASE_TYPE` | 数据库类型 | `sqlite` |
| `SQLITE_DB_PATH` | SQLite 数据库路径 | `explode_word.db` |
| `MYSQL_HOST` | MySQL 主机 | `localhost` |
| `MYSQL_PORT` | MySQL 端口 | `3306` |
| `MYSQL_USERNAME` | MySQL 用户名 | `root` |
| `MYSQL_PASSWORD` | MySQL 密码 | 空 |
| `MYSQL_DATABASE` | MySQL 数据库名 | `explode_word` |

## 开发说明

### 添加新的 API 接口

1. 在相应的 API 模块中添加路由函数
2. 使用适当的装饰器（如 `@jwt_required()`）
3. 返回 JSON 格式的响应

### 添加新的数据模型

1. 在 `app/models/` 目录下创建模型文件
2. 继承 `db.Model` 类
3. 在 `app/models/__init__.py` 中导入新模型

### 数据库操作

```python
from app import db
from app.models.user import User

# 查询
user = User.query.get(1)
users = User.query.filter_by(is_active=True).all()

# 添加
new_user = User(username='test', email='test@example.com')
db.session.add(new_user)
db.session.commit()

# 更新
user.nickname = 'New Nickname'
db.session.commit()

# 删除
db.session.delete(user)
db.session.commit()
```

## 部署说明

### 生产环境配置

1. 设置环境变量：
   ```bash
   export FLASK_ENV=production
   export DATABASE_TYPE=mysql
   ```

2. 使用 Gunicorn 启动：
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 许可证

MIT License