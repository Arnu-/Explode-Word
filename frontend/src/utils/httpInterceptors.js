/**
 * HTTP 拦截器
 * 处理认证、错误重定向等
 */

import { apiClient } from './api.js'
import router from '@/router/index.js'

// 不需要认证的路径
const PUBLIC_PATHS = [
  '/auth/login',
  '/auth/register'
]

/**
 * 检查路径是否需要认证
 * @param {string} url - 请求路径
 * @returns {boolean} 是否需要认证
 */
function requiresAuth(url) {
  return !PUBLIC_PATHS.some(path => url.includes(path))
}

/**
 * 请求拦截器
 * 自动添加认证头部
 */
function requestInterceptor(config) {
  const token = localStorage.getItem('explode_word_token')
  
  // 如果有 token 且请求需要认证，则添加 Authorization 头部
  if (token && requiresAuth(config.url || '')) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  
  return config
}

/**
 * 响应拦截器
 * 处理认证错误和自动重定向
 */
async function responseInterceptor(response, requestConfig) {
  // 如果响应正常，直接返回
  if (response.ok) {
    return response
  }
  
  // 处理认证相关错误
  if (response.status === 401 || response.status === 403) {
    // 清除本地存储的认证信息
    localStorage.removeItem('explode_word_token')
    localStorage.removeItem('explode_word_user')
    
    // 如果不是登录页面的请求，则重定向到登录页
    const currentPath = router.currentRoute.value.path
    if (currentPath !== '/login' && requiresAuth(requestConfig.url || '')) {
      // 保存当前路径，登录后可以重定向回来
      const redirectPath = currentPath !== '/' ? currentPath : '/game'
      
      // 延迟执行重定向，避免在请求过程中立即跳转
      setTimeout(() => {
        router.push({
          path: '/login',
          query: { redirect: redirectPath }
        })
      }, 100)
      
      // 显示错误提示
      console.warn('认证失效，请重新登录')
      
      // 可以在这里触发全局的错误提示
      if (window.__showErrorMessage) {
        window.__showErrorMessage('登录已过期，请重新登录')
      }
    }
  }
  
  return response
}

/**
 * 初始化 HTTP 拦截器
 */
export function setupHttpInterceptors() {
  // 添加请求拦截器
  apiClient.addRequestInterceptor(requestInterceptor)
  
  // 添加响应拦截器
  apiClient.addResponseInterceptor(responseInterceptor)
  
  console.log('HTTP 拦截器已初始化')
}

/**
 * 手动处理认证错误
 * 可以在组件中调用此方法
 */
export function handleAuthError() {
  // 清除认证信息
  localStorage.removeItem('explode_word_token')
  localStorage.removeItem('explode_word_user')
  
  // 重定向到登录页
  const currentPath = router.currentRoute.value.path
  if (currentPath !== '/login') {
    router.push({
      path: '/login',
      query: { redirect: currentPath !== '/' ? currentPath : '/game' }
    })
  }
}

/**
 * 检查并处理 API 响应错误
 * @param {Error} error - 错误对象
 * @returns {boolean} 是否已处理
 */
export function handleApiError(error) {
  if (error.status === 401 || error.status === 403) {
    handleAuthError()
    return true
  }
  
  // 处理其他常见错误
  switch (error.status) {
    case 400:
      console.error('请求参数错误:', error.message)
      break
    case 404:
      console.error('请求的资源不存在:', error.message)
      break
    case 500:
      console.error('服务器内部错误:', error.message)
      break
    default:
      console.error('请求失败:', error.message)
  }
  
  return false
}

export default {
  setupHttpInterceptors,
  handleAuthError,
  handleApiError
}