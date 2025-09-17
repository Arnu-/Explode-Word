/**
 * API 配置和请求工具
 */

import { API_BASE_URL, API_TIMEOUT } from '@/config/env.js'

// API 基础配置
const API_CONFIG = {
  // 根据环境配置自动选择 API 地址
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
}

/**
 * 创建请求实例
 */
class ApiClient {
  constructor(config = {}) {
    this.baseURL = config.baseURL || API_CONFIG.baseURL
    this.timeout = config.timeout || API_CONFIG.timeout
    this.defaultHeaders = {}
    this.interceptors = {
      request: [],
      response: []
    }
    this.authErrorHandler = null
  }

  /**
   * 设置默认请求头
   * @param {string} key - 头部键名
   * @param {string} value - 头部值
   */
  setDefaultHeader(key, value) {
    this.defaultHeaders[key] = value
  }

  /**
   * 移除默认请求头
   * @param {string} key - 头部键名
   */
  removeDefaultHeader(key) {
    delete this.defaultHeaders[key]
  }

  /**
   * 添加请求拦截器
   * @param {Function} interceptor - 拦截器函数
   */
  addRequestInterceptor(interceptor) {
    this.interceptors.request.push(interceptor)
  }

  /**
   * 添加响应拦截器
   * @param {Function} interceptor - 拦截器函数
   */
  addResponseInterceptor(interceptor) {
    this.interceptors.response.push(interceptor)
  }

  /**
   * 设置认证错误处理器
   * @param {Function} handler - 错误处理函数
   */
  setAuthErrorHandler(handler) {
    this.authErrorHandler = handler
  }

  /**
   * 处理认证错误
   */
  handleAuthError() {
    if (this.authErrorHandler) {
      this.authErrorHandler()
    }
  }

  /**
   * 发送 HTTP 请求
   * @param {string} url - 请求路径
   * @param {Object} options - 请求选项
   * @returns {Promise} 请求结果
   */
  async request(url, options = {}) {
    const {
      method = 'GET',
      headers = {},
      body = null,
      ...otherOptions
    } = options

    // 构建完整的请求 URL
    const fullUrl = url.startsWith('http') ? url : `${this.baseURL}${url}`

    // 合并默认请求头
    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...this.defaultHeaders,
      ...headers
    }

    // 构建请求配置
    let requestConfig = {
      method,
      headers: defaultHeaders,
      ...otherOptions
    }

    // 如果有请求体且不是 FormData，则序列化为 JSON
    if (body && !(body instanceof FormData)) {
      requestConfig.body = JSON.stringify(body)
    } else if (body) {
      requestConfig.body = body
      // FormData 时移除 Content-Type，让浏览器自动设置
      delete requestConfig.headers['Content-Type']
    }

    try {
      // 执行请求拦截器
      for (const interceptor of this.interceptors.request) {
        requestConfig = await interceptor(requestConfig) || requestConfig
      }

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), this.timeout)

      const response = await fetch(fullUrl, {
        ...requestConfig,
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      // 执行响应拦截器
      let processedResponse = response
      for (const interceptor of this.interceptors.response) {
        processedResponse = await interceptor(processedResponse, requestConfig) || processedResponse
      }

      // 检查响应状态
      if (!processedResponse.ok) {
        const error = new Error(`HTTP Error: ${processedResponse.status} ${processedResponse.statusText}`)
        error.status = processedResponse.status
        error.response = processedResponse
        throw error
      }

      // 尝试解析 JSON 响应
      const contentType = processedResponse.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        const jsonData = await processedResponse.json()
        return jsonData
      }

      return await processedResponse.text()
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('请求超时')
      }
      
      // 处理 HTTP 错误状态码
      if (error.status) {
        switch (error.status) {
          case 401:
            error.message = '未授权访问，请重新登录'
            // 触发登录跳转事件
            this.handleAuthError()
            break
          case 403:
            error.message = '权限不足，拒绝访问'
            break
          case 404:
            error.message = '请求的资源不存在'
            break
          case 422:
            error.message = '请求参数错误或用户未认证'
            // 422通常表示JWT token无效或过期
            this.handleAuthError()
            break
          case 500:
            error.message = '服务器内部错误'
            break
          default:
            if (error.status >= 400 && error.status < 500) {
              error.message = '客户端请求错误'
            } else if (error.status >= 500) {
              error.message = '服务器错误'
            }
        }
      }
      
      throw error
    }
  }

  // 便捷方法
  get(url, options = {}) {
    return this.request(url, { ...options, method: 'GET' })
  }

  post(url, data, options = {}) {
    return this.request(url, { ...options, method: 'POST', body: data })
  }

  put(url, data, options = {}) {
    return this.request(url, { ...options, method: 'PUT', body: data })
  }

  delete(url, options = {}) {
    return this.request(url, { ...options, method: 'DELETE' })
  }

  patch(url, data, options = {}) {
    return this.request(url, { ...options, method: 'PATCH', body: data })
  }
}

// 创建默认的 API 客户端实例
export const apiClient = new ApiClient()

// 导出 API 配置
export { API_CONFIG }

// 导出类以便创建自定义实例
export default ApiClient