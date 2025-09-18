# Explode Word - 单词爆破游戏

<div align="center">

![Explode Word Logo](frontend/public/logo.jpeg)

**一个现代化的单词学习游戏平台**

[![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

## 📖 项目简介

Explode Word 是一个集学习与娱乐于一体的单词学习游戏平台。通过游戏化的方式帮助用户学习英语单词，提供丰富的关卡挑战、词汇管理和个人成长追踪功能。

> 🤖 **特别说明**: 本项目完全通过 [CodeBuddy](https://codebuddy.ai) AI 编程助手，采用对话驱动的方式开发完成。从前端 Vue.js 应用到后端 Flask API，从数据库设计到用户界面，每一行代码都是通过与 AI 的智能对话生成的，展示了 AI 辅助编程的强大能力。

### ✨ 核心特性

- 🎮 **游戏化学习** - 通过关卡挑战的方式学习单词
- 📚 **词汇管理** - 自定义词库和单词分组
- 📊 **数据统计** - 详细的学习进度和成绩分析
- 🏆 **成就系统** - 多样化的成就徽章激励学习
- 👤 **用户档案** - 个人信息管理和学习历史
- 📱 **响应式设计** - 支持多种设备和屏幕尺寸

## 🛠️ 技术架构

> 💡 **开发方式**: 本项目采用 **AI 对话驱动开发**，通过与 [CodeBuddy](https://codebuddy.ai) 的智能对话完成整个技术栈的实现。

### 前端技术栈

- **框架**: Vue 3 (Composition API) - *AI 生成的现代化组件*
- **构建工具**: Vite 7.x - *智能配置和优化*
- **路由**: Vue Router 4 - *AI 设计的路由架构*
- **状态管理**: Vue 3 Reactivity API - *响应式状态管理*
- **样式**: CSS3 + 自定义主题系统 - *AI 生成的美观界面*
- **图标**: Font Awesome - *丰富的图标库*
- **HTTP客户端**: 自定义 Fetch API 封装 - *智能错误处理*

### 后端技术栈

- **框架**: Flask 2.x - *AI 构建的轻量级后端*
- **数据库**: SQLite (开发) / PostgreSQL (生产) - *智能数据库设计*
- **ORM**: SQLAlchemy - *AI 生成的数据模型*
- **认证**: JWT (Flask-JWT-Extended) - *安全的用户认证*
- **数据迁移**: Flask-Migrate - *自动化数据库迁移*
- **跨域**: Flask-CORS - *智能跨域配置*
- **API文档**: 自定义接口文档 - *AI 生成的完整API*

### 🤖 AI 开发特色

- **对话式开发** - 通过自然语言描述需求，AI 自动生成代码
- **智能架构设计** - AI 提供最佳实践和现代化架构建议
- **自动化测试** - AI 生成测试用例和验证脚本
- **代码优化** - 持续的代码质量改进和性能优化
- **问题解决** - 智能调试和错误修复

### 项目结构

```
Explode-Word/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   │   ├── common/     # 通用组件
│   │   │   ├── levels/     # 关卡相关组件
│   │   │   └── vocabulary/ # 词汇管理组件
│   │   ├── pages/          # 页面组件
│   │   ├── services/       # API服务层
│   │   ├── utils/          # 工具函数
│   │   ├── assets/         # 静态资源
│   │   └── router/         # 路由配置
│   ├── public/             # 公共资源
│   └── package.json        # 依赖配置
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   └── utils/          # 工具函数
│   ├── config/             # 配置文件
│   ├── migrations/         # 数据库迁移
│   └── requirements.txt    # Python依赖
└── assets/                 # 项目资源文件
```

## 🚀 快速开始

### 环境要求

- **Node.js**: >= 16.0.0
- **Python**: >= 3.8
- **npm**: >= 8.0.0
- **Git**: 最新版本

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/Arnu-/Explode-Word.git
cd Explode-Word
```

#### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 创建测试用户（可选）
python create_test_user.py

# 启动后端服务
python run.py
```

后端服务将在 `http://localhost:5000` 启动

#### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 🔧 开发环境配置

#### 后端配置

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///explode_word.db

# JWT配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
```

#### 前端配置

Vite 会自动处理开发环境的代理配置，API请求会自动转发到后端服务。

## 📱 功能模块

### 🎯 游戏系统

- **关卡挑战**: 多难度级别的单词挑战
- **计时模式**: 限时答题增加挑战性
- **分数系统**: 基于准确率和速度的评分
- **星级评价**: 三星评价系统

### 📚 词汇管理

- **词库管理**: 创建和管理自定义词库
- **单词分组**: 按主题或难度分组单词
- **批量导入**: 支持CSV格式批量导入单词
- **词汇搜索**: 快速查找和编辑单词

### 👤 用户系统

- **用户注册/登录**: JWT认证系统
- **个人档案**: 用户信息管理
- **学习统计**: 详细的学习数据分析
- **成就系统**: 多种成就徽章

### 📊 数据分析

- **学习进度**: 可视化学习进度追踪
- **成绩统计**: 历史成绩和趋势分析
- **排行榜**: 用户排名和竞争
- **学习报告**: 定期学习报告生成

## 🎮 使用指南

### 新用户入门

1. **注册账户**: 访问登录页面创建新账户
2. **选择关卡**: 从关卡选择页面开始第一个挑战
3. **开始游戏**: 根据提示完成单词挑战
4. **查看进度**: 在个人档案页面查看学习统计

### 词汇管理

1. **创建词库**: 在词汇管理页面创建新的词库
2. **添加单词**: 手动添加或批量导入单词
3. **组织分组**: 将单词按主题或难度分组
4. **开始学习**: 基于自定义词库创建游戏

### 个人档案

- **基本信息**: 编辑用户名、邮箱等信息
- **学习统计**: 查看总游戏次数、平均分数等
- **游戏历史**: 浏览历史游戏记录
- **成就展示**: 查看已解锁的成就徽章

## 🔌 API 接口

### 认证接口

```http
POST /api/auth/register    # 用户注册
POST /api/auth/login       # 用户登录
POST /api/auth/logout      # 用户登出
GET  /api/auth/me          # 获取当前用户信息
```

### 用户接口

```http
GET  /api/users/profile    # 获取用户档案
PUT  /api/users/profile    # 更新用户档案
GET  /api/users/stats      # 获取用户统计
GET  /api/users/leaderboard # 获取排行榜
```

### 游戏接口

```http
GET  /api/levels/          # 获取关卡列表
GET  /api/levels/{id}      # 获取关卡详情
POST /api/levels/{id}/start # 开始关卡
POST /api/levels/{id}/complete # 完成关卡
```

### 词汇接口

```http
GET  /api/vocabulary/libraries    # 获取词库列表
POST /api/vocabulary/libraries    # 创建词库
GET  /api/vocabulary/groups       # 获取词组列表
POST /api/vocabulary/words        # 添加单词
```

## 🧪 测试

### 后端测试

```bash
cd backend

# 运行API测试
python test_user_profile_api.py
python test_levels_api.py
python test_vocabulary_api.py

# 运行单元测试
python -m pytest tests/
```

### 前端测试

```bash
cd frontend

# 运行单元测试
npm run test

# 运行E2E测试
npm run test:e2e
```

## 📦 部署

### 生产环境构建

#### 前端构建

```bash
cd frontend
npm run build
```

构建文件将生成在 `frontend/dist/` 目录。

#### 后端部署

```bash
cd backend

# 设置生产环境变量
export FLASK_ENV=production

# 运行数据库迁移
flask db upgrade

# 启动生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

1. **Fork** 项目到你的GitHub账户
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **创建** Pull Request

### 代码规范

- **前端**: 遵循 Vue.js 官方风格指南
- **后端**: 遵循 PEP 8 Python 代码规范
- **提交**: 使用语义化提交信息

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

### 🤖 特别感谢 CodeBuddy AI

本项目的成功开发离不开 **[CodeBuddy](https://codebuddy.ai)** 的强大支持：

- 🎯 **智能代码生成** - 通过自然语言对话生成高质量代码
- 🔧 **全栈开发支持** - 从前端到后端的完整技术栈覆盖
- 🐛 **智能调试** - 快速定位和解决代码问题
- 📚 **最佳实践指导** - 提供现代化的开发模式和架构建议
- 🚀 **效率提升** - 大幅缩短开发周期，提高代码质量

> **CodeBuddy** 让编程变得更加智能和高效，是现代开发者的得力助手！

### 🛠️ 技术框架致谢

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级Python Web框架
- [Font Awesome](https://fontawesome.com/) - 图标库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具

## 📞 联系我们

- **项目主页**: [GitHub Repository](https://github.com/Arnu-/Explode-Word)
- **问题反馈**: [Issues](https://github.com/Arnu-/Explode-Word/issues)
- **功能建议**: [Discussions](https://github.com/Arnu-/Explode-Word/discussions)

## 📈 项目状态

- ✅ **核心功能**: 已完成
- ✅ **用户系统**: 已完成
- ✅ **词汇管理**: 已完成
- ✅ **数据统计**: 已完成
- 🚧 **丰富词库**: 进行中
- 📋 **词库集市**: 计划中

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐️**

Made with ❤️ by [Arnu] & 🤖 **[CodeBuddy AI](https://codebuddy.ai)**

*本项目完全通过 AI 对话驱动开发，展示了人工智能在软件开发领域的无限可能*

</div>