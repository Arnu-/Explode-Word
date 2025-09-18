/**
 * 环境配置文件
 * 根据不同环境配置不同的 API 地址和其他配置
 */

// 获取当前环境
const getEnv = () => {
  return import.meta.env.MODE || 'development'
}

// 判断是否为开发环境
export const isDev = () => {
  return getEnv() === 'development'
}

// 判断是否为生产环境
export const isProd = () => {
  return getEnv() === 'production'
}

// 环境配置
const envConfig = {
  development: {
    // 开发环境：使用 Vite 代理
    API_BASE_URL: '/api',
    API_TIMEOUT: 10000,
    ENABLE_MOCK: false,
    LOG_LEVEL: 'debug'
  },
  production: {
    // 生产环境：已经通过nginx代理到api路径了。
    API_BASE_URL: '/api',
    API_TIMEOUT: 15000,
    ENABLE_MOCK: false,
    LOG_LEVEL: 'error'
  },
  test: {
    // 测试环境：使用 Vite 代理
    API_BASE_URL: '/api',
    API_TIMEOUT: 8000,
    ENABLE_MOCK: true,
    LOG_LEVEL: 'warn'
  }
}

// 获取当前环境配置
export const getConfig = () => {
  const env = getEnv()
  return envConfig[env] || envConfig.development
}

// 导出具体配置项
export const {
  API_BASE_URL,
  API_TIMEOUT,
  ENABLE_MOCK,
  LOG_LEVEL
} = getConfig()

// 导出环境信息
export const ENV = getEnv()

// 调试信息（仅在开发环境输出）
if (isDev()) {
  console.log('🚀 当前环境:', ENV)
  console.log('📡 API 地址:', API_BASE_URL)
  console.log('⏱️ 请求超时:', API_TIMEOUT + 'ms')
}