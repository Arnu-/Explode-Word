# 🔐 认证问题修复指南

## 问题描述
前端主页的 profile 接口返回 422 错误，表示用户未认证或 token 无效，需要自动跳转到登录页面。

## 🛠️ 修复内容

### 1. API 客户端增强 (`frontend/src/utils/api.js`)
- ✅ 添加自动认证失败检测
- ✅ 401/422 错误自动跳转登录页面
- ✅ 自动清理无效 token
- ✅ 支持自定义认证失败回调

### 2. 认证管理器优化 (`frontend/src/utils/auth.js`)
- ✅ 增强错误处理机制
- ✅ 自动跳转到登录页面
- ✅ 保存跳转前的页面路径
- ✅ 更好的用户体验提示

### 3. 路由守卫系统 (`frontend/src/utils/routeGuard.js`)
- ✅ 统一的认证检查逻辑
- ✅ 自动保存和恢复跳转路径
- ✅ 认证状态实时验证

### 4. 认证检查组件 (`frontend/src/components/common/AuthCheck.vue`)
- ✅ 可复用的认证状态检查
- ✅ 优雅的加载和错误状态
- ✅ 自动重定向功能

## 🚀 使用方法

### 方法一：在路由中使用守卫
```javascript
// router/index.js
import { authGuard } from '@/utils/routeGuard.js'

const router = createRouter({
  // ... 路由配置
})

// 添加全局前置守卫
router.beforeEach(authGuard)

// 在路由元信息中标记需要认证的页面
{
  path: '/dashboard',
  component: Dashboard,
  meta: { requiresAuth: true }
}
```

### 方法二：在组件中使用 AuthCheck
```vue
<template>
  <AuthCheck>
    <!-- 需要认证的内容 -->
    <Dashboard />
  </AuthCheck>
</template>

<script>
import AuthCheck from '@/components/common/AuthCheck.vue'
import Dashboard from '@/pages/Dashboard.vue'

export default {
  components: {
    AuthCheck,
    Dashboard
  }
}
</script>
```

### 方法三：手动检查认证状态
```javascript
import { checkAuthStatus } from '@/utils/routeGuard.js'

async function someFunction() {
  const isAuthenticated = await checkAuthStatus()
  if (!isAuthenticated) {
    // 用户未认证，会自动跳转到登录页面
    return
  }
  
  // 继续执行需要认证的操作
}
```

## 🔧 自动跳转逻辑

### 触发条件
- API 返回 401 (未授权)
- API 返回 422 (token 无效)
- 手动调用认证检查失败

### 跳转行为
1. 自动清理本地存储的无效 token
2. 保存当前页面路径到 `redirect_after_login`
3. 跳转到 `/login` 页面
4. 显示友好的错误提示

### 登录后恢复
```javascript
import { handleLoginRedirect } from '@/utils/routeGuard.js'

// 在登录成功后调用
const redirectPath = handleLoginRedirect()
router.push(redirectPath) // 跳转回原来的页面
```

## 📱 用户体验改进

### 加载状态
- 认证检查时显示加载动画
- 避免页面闪烁和空白状态

### 错误提示
- 清晰的错误信息说明
- 一键重新登录按钮
- 自动跳转倒计时（可选）

### 路径保存
- 自动保存用户访问的目标页面
- 登录后自动跳转回原页面
- 避免用户重复导航

## 🧪 测试验证

### 测试场景
1. **未登录访问受保护页面** → 自动跳转登录
2. **Token 过期** → 自动清理并跳转登录
3. **网络错误** → 显示错误提示，不跳转
4. **登录成功** → 跳转回原页面

### 测试命令
```bash
# 清理本地存储测试未登录状态
localStorage.clear()

# 设置过期 token 测试自动清理
localStorage.setItem('access_token', 'expired_token')

# 测试 API 调用
curl -H "Authorization: Bearer invalid_token" http://localhost:5173/api/auth/profile
```

## 🎯 核心优势

1. **自动化处理** - 无需手动检查认证状态
2. **用户友好** - 优雅的错误处理和跳转
3. **开发便利** - 统一的认证逻辑，易于维护
4. **灵活配置** - 支持多种使用方式
5. **状态保持** - 自动保存和恢复用户路径

现在当用户遇到 422 认证错误时，系统会自动：
- 清理无效的认证信息
- 显示友好的提示信息
- 跳转到登录页面
- 登录成功后跳转回原页面

这样就解决了你遇到的认证问题！🎉