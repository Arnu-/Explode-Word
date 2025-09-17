# 登录系统实现说明

本项目已实现完整的 JWT 认证登录系统，包括前端登录页面、token 管理、API 拦截器和路由守卫等功能。

## 功能特性

### 🔐 认证功能
- ✅ 用户登录/注册
- ✅ JWT Token 管理
- ✅ 自动 Token 刷新机制
- ✅ 安全的密码处理
- ✅ 记住登录状态

### 🛡️ 安全机制
- ✅ 路由守卫（未登录自动跳转）
- ✅ API 请求拦截器
- ✅ 401/403 错误自动处理
- ✅ Token 过期自动重定向
- ✅ 本地存储安全管理

### 🎨 用户界面
- ✅ 现代化登录页面
- ✅ 用户仪表板
- ✅ 个人资料管理
- ✅ 密码修改功能
- ✅ 响应式设计

## 文件结构

```
frontend/src/
├── pages/
│   ├── Login.vue           # 登录/注册页面
│   ├── Dashboard.vue       # 用户仪表板
│   └── Profile.vue         # 个人资料页面
├── utils/
│   ├── auth.js            # 认证管理器
│   ├── api.js             # API 客户端（已增强）
│   └── httpInterceptors.js # HTTP 拦截器
├── config/
│   └── env.js             # 环境配置
└── router/
    └── index.js           # 路由配置（含守卫）
```

## 后端 API 接口

### 认证相关接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户注册 | POST | `/api/auth/register` | 新用户注册 |
| 用户登录 | POST | `/api/auth/login` | 用户登录 |
| 获取用户信息 | GET | `/api/auth/profile` | 获取当前用户信息 |
| 更新用户信息 | PUT | `/api/auth/profile` | 更新用户资料 |
| 修改密码 | POST | `/api/auth/change-password` | 修改用户密码 |

### 请求/响应格式

#### 登录请求
```json
{
  "username": "用户名或邮箱",
  "password": "密码"
}
```

#### 登录响应
```json
{
  "message": "登录成功",
  "access_token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "测试用户",
    "total_games": 0,
    "total_wins": 0,
    "win_rate": 0,
    "best_score": 0
  }
}
```

## 前端使用方法

### 1. 认证状态管理

```javascript
import { useAuth } from '@/utils/auth.js'

export default {
  setup() {
    const { user, isAuthenticated, login, logout } = useAuth()
    
    // 检查登录状态
    console.log('是否已登录:', isAuthenticated.value)
    console.log('当前用户:', user.value)
    
    // 登录
    const handleLogin = async () => {
      const result = await login({
        username: 'testuser',
        password: 'password123'
      })
      
      if (result.success) {
        console.log('登录成功')
      } else {
        console.error('登录失败:', result.error)
      }
    }
    
    return { user, isAuthenticated, handleLogin, logout }
  }
}
```

### 2. API 请求

```javascript
import { apiClient } from '@/utils/api.js'

// 自动携带 Authorization 头部
const getUserData = async () => {
  try {
    const response = await apiClient.get('/auth/profile')
    return response.user
  } catch (error) {
    // 401/403 错误会自动重定向到登录页
    console.error('请求失败:', error.message)
  }
}
```

### 3. 路由保护

```javascript
// 在路由配置中设置 meta.requiresAuth
{
  path: '/dashboard',
  component: Dashboard,
  meta: { requiresAuth: true }  // 需要登录才能访问
}
```

## 启动和测试

### 1. 启动后端服务

```bash
cd backend
python run.py
```

后端服务将在 `http://127.0.0.1:5000` 启动。

### 2. 启动前端服务

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

### 3. 测试流程

1. **访问首页** - 自动重定向到登录页面
2. **注册新用户** - 点击"立即注册"，填写信息
3. **登录系统** - 使用用户名/邮箱和密码登录
4. **访问仪表板** - 登录成功后查看用户统计
5. **编辑资料** - 在个人资料页面更新信息
6. **测试保护** - 尝试直接访问受保护页面
7. **退出登录** - 点击退出按钮，验证重定向

## 安全特性详解

### 1. Token 管理
- Token 存储在 `localStorage` 中
- 自动在请求头中添加 `Authorization: Bearer <token>`
- 登出时自动清除本地存储

### 2. 路由守卫
- 未登录用户访问受保护页面自动重定向到登录页
- 已登录用户访问登录页自动重定向到仪表板
- 支持登录后重定向到原目标页面

### 3. API 拦截器
- 自动处理 401/403 错误
- 错误时清除本地认证信息
- 自动重定向到登录页面

### 4. 错误处理
- 网络错误友好提示
- 表单验证和错误显示
- 加载状态指示器

## 自定义配置

### 1. 修改 API 地址

编辑 `src/config/env.js`：

```javascript
const envConfig = {
  development: {
    API_BASE_URL: '/api',  // 开发环境使用代理
    API_TIMEOUT: 10000
  },
  production: {
    API_BASE_URL: 'https://your-api-domain.com/api',  // 生产环境直接访问
    API_TIMEOUT: 15000
  }
}
```

### 2. 修改 Token 存储

编辑 `src/utils/auth.js`：

```javascript
// 修改存储键名
const TOKEN_KEY = 'your_app_token'
const USER_KEY = 'your_app_user'

// 或者使用 sessionStorage（关闭浏览器后失效）
sessionStorage.setItem(TOKEN_KEY, accessToken)
```

### 3. 自定义路由守卫

编辑 `src/router/index.js`：

```javascript
router.beforeEach((to, from, next) => {
  // 添加自定义逻辑
  const isAuthenticated = authManager.isAuthenticated
  
  // 例如：管理员页面需要特殊权限
  if (to.meta.requiresAdmin && !user.isAdmin) {
    next('/dashboard')
    return
  }
  
  // 其他逻辑...
})
```

## 故障排除

### 常见问题

1. **登录后立即跳转到登录页**
   - 检查后端 JWT 配置
   - 确认 token 格式正确
   - 查看浏览器控制台错误

2. **API 请求 CORS 错误**
   - 确认后端 CORS 配置
   - 检查 Vite 代理设置
   - 验证请求头格式

3. **路由守卫不生效**
   - 确认路由 meta 配置
   - 检查 authManager 初始化
   - 验证 localStorage 数据

### 调试技巧

1. **查看认证状态**
```javascript
console.log('认证状态:', authManager.isAuthenticated)
console.log('当前用户:', authManager.currentUser)
console.log('Token:', authManager.currentToken)
```

2. **查看本地存储**
```javascript
console.log('Token:', localStorage.getItem('explode_word_token'))
console.log('User:', localStorage.getItem('explode_word_user'))
```

3. **网络请求调试**
- 打开浏览器开发者工具
- 查看 Network 面板
- 检查请求头和响应

## 扩展功能

### 可以添加的功能

1. **记住我功能** - 延长 token 有效期
2. **多设备登录管理** - 显示登录设备列表
3. **第三方登录** - 支持 Google、GitHub 等
4. **双因素认证** - 增强安全性
5. **密码强度检测** - 实时密码强度提示
6. **登录历史** - 记录登录时间和 IP

### 性能优化

1. **Token 自动刷新** - 在过期前自动刷新
2. **请求缓存** - 缓存用户信息请求
3. **懒加载** - 按需加载认证相关组件
4. **状态持久化** - 使用 Pinia 管理全局状态

## 总结

本登录系统提供了完整的用户认证解决方案，具有以下优势：

- 🔒 **安全可靠** - JWT 认证 + 多层安全防护
- 🎨 **用户友好** - 现代化 UI + 流畅交互
- 🛠️ **易于维护** - 模块化设计 + 清晰架构
- 📱 **响应式** - 支持各种设备尺寸
- 🔧 **可扩展** - 灵活的配置和扩展机制

系统已经可以投入使用，并且可以根据具体需求进行进一步的定制和扩展。