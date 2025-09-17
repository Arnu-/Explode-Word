/**
 * 路由守卫 - 处理认证检查和自动跳转
 */

import { authManager } from './auth.js'

/**
 * 认证路由守卫
 * @param {Object} to - 目标路由
 * @param {Object} from - 来源路由
 * @param {Function} next - 下一步函数
 */
export function authGuard(to, from, next) {
  // 检查是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  if (requiresAuth) {
    if (authManager.isAuthenticated) {
      // 已认证，允许访问
      next()
    } else {
      // 未认证，跳转到登录页面
      console.warn('访问受保护页面需要登录，跳转到登录页面')
      
      // 保存目标路径，登录后跳转回来
      if (to.path !== '/login') {
        localStorage.setItem('redirect_after_login', to.fullPath)
      }
      
      next('/login')
    }
  } else {
    // 不需要认证，直接允许访问
    next()
  }
}

/**
 * 登录后重定向处理
 */
export function handleLoginRedirect() {
  const redirectPath = localStorage.getItem('redirect_after_login')
  if (redirectPath) {
    localStorage.removeItem('redirect_after_login')
    return redirectPath
  }
  return '/game' // 默认跳转到游戏页面
}

/**
 * 检查并刷新用户认证状态
 */
export async function checkAuthStatus() {
  if (authManager.isAuthenticated) {
    try {
      // 尝试获取最新用户信息来验证token是否有效
      const result = await authManager.getCurrentUser()
      return result.success
    } catch (error) {
      console.error('认证状态检查失败:', error)
      return false
    }
  }
  return false
}