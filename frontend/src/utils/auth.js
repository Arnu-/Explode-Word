/**
 * 认证工具类
 * 处理 token 存储、用户状态管理等
 */

import { ref, computed } from 'vue'
import { apiClient } from './api.js'

// 响应式用户状态
const user = ref(null)
const token = ref(null)

// Token 存储键名
const TOKEN_KEY = 'explode_word_token'
const USER_KEY = 'explode_word_user'

/**
 * 认证管理类
 */
class AuthManager {
  constructor() {
    this.initializeAuth()
    this.setupApiErrorHandler()
  }

  /**
   * 初始化认证状态
   */
  initializeAuth() {
    // 从 localStorage 恢复 token 和用户信息
    const savedToken = localStorage.getItem(TOKEN_KEY)
    const savedUser = localStorage.getItem(USER_KEY)

    if (savedToken && savedUser) {
      try {
        token.value = savedToken
        user.value = JSON.parse(savedUser)
        // 设置 API 客户端的默认 Authorization 头
        this.setAuthHeader(savedToken)
      } catch (error) {
        console.error('恢复用户状态失败:', error)
        this.clearAuth()
      }
    }
  }

  /**
   * 设置API错误处理器
   */
  setupApiErrorHandler() {
    // 设置API客户端的认证错误处理器
    apiClient.setAuthErrorHandler(() => {
      console.warn('检测到认证错误，自动跳转到登录页面')
      this.handleAuthError()
    })
  }

  /**
   * 处理认证错误
   */
  handleAuthError() {
    // 清除认证信息
    this.clearAuth()
    
    // 跳转到登录页面
    if (typeof window !== 'undefined' && window.location) {
      // 保存当前页面路径，登录后可以跳转回来
      const currentPath = window.location.pathname
      if (currentPath !== '/login' && currentPath !== '/') {
        localStorage.setItem('redirect_after_login', currentPath)
      }
      
      // 跳转到登录页面
      window.location.href = '/login'
    }
  }

  /**
   * 用户登录
   * @param {Object} credentials - 登录凭据
   * @returns {Promise} 登录结果
   */
  async login(credentials) {
    try {
      const response = await apiClient.post('/auth/login', credentials)
      
      if (response.access_token && response.user) {
        // 保存 token 和用户信息
        this.setAuth(response.access_token, response.user)
        return { success: true, data: response }
      } else {
        throw new Error('登录响应格式错误')
      }
    } catch (error) {
      console.error('登录失败:', error)
      return { 
        success: false, 
        error: error.message || '登录失败，请检查用户名和密码' 
      }
    }
  }

  /**
   * 用户注册
   * @param {Object} userData - 注册数据
   * @returns {Promise} 注册结果
   */
  async register(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData)
      
      if (response.access_token && response.user) {
        // 注册成功后自动登录
        this.setAuth(response.access_token, response.user)
        return { success: true, data: response }
      } else {
        throw new Error('注册响应格式错误')
      }
    } catch (error) {
      console.error('注册失败:', error)
      return { 
        success: false, 
        error: error.message || '注册失败，请稍后重试' 
      }
    }
  }

  /**
   * 用户登出
   */
  logout() {
    this.clearAuth()
    // 可以调用后端登出接口（如果需要）
    // apiClient.post('/auth/logout').catch(() => {})
  }

  /**
   * 获取当前用户信息
   * @returns {Promise} 用户信息
   */
  async getCurrentUser() {
    try {
      const response = await apiClient.get('/auth/profile')
      if (response.user) {
        user.value = response.user
        this.saveUserToStorage(response.user)
        return { success: true, data: response.user }
      }
      throw new Error('获取用户信息失败')
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取用户信息失败，可能是 token 过期
      if (error.status === 401 || error.status === 403 || error.status === 422) {
        this.handleAuthError()
      }
      return { success: false, error: error.message }
    }
  }

  /**
   * 更新用户信息
   * @param {Object} userData - 用户数据
   * @returns {Promise} 更新结果
   */
  async updateProfile(userData) {
    try {
      const response = await apiClient.put('/auth/profile', userData)
      if (response.user) {
        user.value = response.user
        this.saveUserToStorage(response.user)
        return { success: true, data: response.user }
      }
      throw new Error('更新用户信息失败')
    } catch (error) {
      console.error('更新用户信息失败:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * 修改密码
   * @param {Object} passwordData - 密码数据
   * @returns {Promise} 修改结果
   */
  async changePassword(passwordData) {
    try {
      const response = await apiClient.post('/auth/change-password', passwordData)
      return { success: true, data: response }
    } catch (error) {
      console.error('修改密码失败:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * 设置认证信息
   * @param {string} accessToken - 访问令牌
   * @param {Object} userData - 用户数据
   */
  setAuth(accessToken, userData) {
    token.value = accessToken
    user.value = userData
    
    // 保存到 localStorage
    localStorage.setItem(TOKEN_KEY, accessToken)
    this.saveUserToStorage(userData)
    
    // 设置 API 请求头
    this.setAuthHeader(accessToken)
  }

  /**
   * 清除认证信息
   */
  clearAuth() {
    token.value = null
    user.value = null
    
    // 清除 localStorage
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    
    // 清除 API 请求头
    this.clearAuthHeader()
  }

  /**
   * 设置 API 请求的 Authorization 头
   * @param {string} accessToken - 访问令牌
   */
  setAuthHeader(accessToken) {
    // 这里需要修改 API 客户端以支持设置默认头部
    if (apiClient.setDefaultHeader) {
      apiClient.setDefaultHeader('Authorization', `Bearer ${accessToken}`)
    }
  }

  /**
   * 清除 API 请求的 Authorization 头
   */
  clearAuthHeader() {
    if (apiClient.removeDefaultHeader) {
      apiClient.removeDefaultHeader('Authorization')
    }
  }

  /**
   * 保存用户信息到存储
   * @param {Object} userData - 用户数据
   */
  saveUserToStorage(userData) {
    localStorage.setItem(USER_KEY, JSON.stringify(userData))
  }

  /**
   * 检查是否已登录
   * @returns {boolean} 是否已登录
   */
  get isAuthenticated() {
    return !!token.value && !!user.value
  }

  /**
   * 获取当前用户
   * @returns {Object|null} 当前用户
   */
  get currentUser() {
    return user.value
  }

  /**
   * 获取当前 token
   * @returns {string|null} 当前 token
   */
  get currentToken() {
    return token.value
  }
}

// 创建认证管理器实例
export const authManager = new AuthManager()

// 导出响应式状态
export const useAuth = () => {
  return {
    user: computed(() => user.value),
    token: computed(() => token.value),
    isAuthenticated: computed(() => authManager.isAuthenticated),
    login: authManager.login.bind(authManager),
    register: authManager.register.bind(authManager),
    logout: authManager.logout.bind(authManager),
    getCurrentUser: authManager.getCurrentUser.bind(authManager),
    updateProfile: authManager.updateProfile.bind(authManager),
    changePassword: authManager.changePassword.bind(authManager)
  }
}

// 导出认证管理器
export default authManager