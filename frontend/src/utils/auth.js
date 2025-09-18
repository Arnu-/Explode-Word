/**
 * 认证工具函数
 */
import { ref, computed } from 'vue'
import { apiClient } from '@/utils/api.js'

// 全局状态
const currentUser = ref(null)
const isAuthenticated = ref(false)
const authToken = ref(null)

// 从localStorage恢复认证状态
const restoreAuthState = () => {
  try {
    const token = localStorage.getItem('auth_token')
    const user = localStorage.getItem('current_user')
    
    if (token && user) {
      authToken.value = token
      currentUser.value = JSON.parse(user)
      isAuthenticated.value = true
      
      // 设置API客户端的默认认证头
      apiClient.setDefaultHeader('Authorization', `Bearer ${token}`)
    }
  } catch (error) {
    console.error('恢复认证状态失败:', error)
    clearAuthState()
  }
}

// 清除认证状态
const clearAuthState = () => {
  currentUser.value = null
  isAuthenticated.value = false
  authToken.value = null
  
  localStorage.removeItem('auth_token')
  localStorage.removeItem('current_user')
  
  // 移除API客户端的认证头
  apiClient.removeDefaultHeader('Authorization')
}

// 设置认证状态
const setAuthState = (token, user) => {
  authToken.value = token
  currentUser.value = user
  isAuthenticated.value = true
  
  // 保存到localStorage
  localStorage.setItem('auth_token', token)
  localStorage.setItem('current_user', JSON.stringify(user))
  
  // 设置API客户端的默认认证头
  apiClient.setDefaultHeader('Authorization', `Bearer ${token}`)
}

// 登录函数
const login = async (credentials) => {
  try {
    const response = await apiClient.post('/auth/login', credentials)
    
    if (response.access_token && response.user) {
      setAuthState(response.access_token, response.user)
      return { success: true, user: response.user }
    } else {
      throw new Error('登录响应格式错误')
    }
  } catch (error) {
    console.error('登录失败:', error)
    throw error
  }
}

// 注册函数
const register = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', userData)
    
    if (response.access_token && response.user) {
      setAuthState(response.access_token, response.user)
      return { success: true, user: response.user }
    } else {
      // 如果注册成功但没有返回token，需要手动登录
      return { success: true, needLogin: true }
    }
  } catch (error) {
    console.error('注册失败:', error)
    throw error
  }
}

// 登出函数
const logout = async () => {
  try {
    // 可以调用后端登出接口
    await apiClient.post('/auth/logout')
  } catch (error) {
    console.warn('后端登出失败:', error)
  } finally {
    clearAuthState()
  }
}

// 刷新token
const refreshToken = async () => {
  try {
    const response = await apiClient.post('/auth/refresh')
    
    if (response.access_token) {
      authToken.value = response.access_token
      localStorage.setItem('auth_token', response.access_token)
      apiClient.setDefaultHeader('Authorization', `Bearer ${response.access_token}`)
      return true
    }
    
    return false
  } catch (error) {
    console.error('刷新token失败:', error)
    clearAuthState()
    return false
  }
}

// 检查认证状态
const checkAuthStatus = async () => {
  if (!authToken.value) {
    return false
  }
  
  try {
    const response = await apiClient.get('/auth/me')
    
    if (response.user) {
      currentUser.value = response.user
      localStorage.setItem('current_user', JSON.stringify(response.user))
      return true
    }
    
    return false
  } catch (error) {
    console.error('检查认证状态失败:', error)
    clearAuthState()
    return false
  }
}

// 设置认证错误处理器
apiClient.setAuthErrorHandler(() => {
  console.warn('认证失效，清除认证状态')
  clearAuthState()
  
  // 可以在这里触发重新登录的逻辑
  // 例如跳转到登录页面
  if (typeof window !== 'undefined' && window.location) {
    const currentPath = window.location.pathname
    if (currentPath !== '/login' && currentPath !== '/register') {
      window.location.href = '/login'
    }
  }
})

// 初始化时恢复认证状态
restoreAuthState()

// 导出认证相关的响应式数据和函数
export const useAuth = () => {
  return {
    // 响应式数据
    currentUser: computed(() => currentUser.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    authToken: computed(() => authToken.value),
    
    // 方法
    login,
    register,
    logout,
    refreshToken,
    checkAuthStatus,
    clearAuthState,
    setAuthState
  }
}

// 导出工具函数
export {
  restoreAuthState,
  clearAuthState,
  setAuthState
}