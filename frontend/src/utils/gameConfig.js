// 游戏配置工具函数

// 默认配置
const DEFAULT_CONFIG = {
  englishFontSize: 18,
  chineseFontSize: 16,
  levelColors: {
    level1: '#e8f5e8',
    level2: '#fff3cd',
    level3: '#ffeaa7',
    level4: '#fab1a0'
  }
}

// 获取游戏配置
export function getGameConfig() {
  try {
    const savedConfig = localStorage.getItem('gameConfig')
    if (savedConfig) {
      const parsed = JSON.parse(savedConfig)
      return { ...DEFAULT_CONFIG, ...parsed }
    }
  } catch (error) {
    console.error('获取游戏配置失败:', error)
  }
  return DEFAULT_CONFIG
}

// 保存游戏配置
export function saveGameConfig(config) {
  try {
    localStorage.setItem('gameConfig', JSON.stringify(config))
    // 触发全局配置更新事件
    window.dispatchEvent(new CustomEvent('gameConfigUpdated', {
      detail: config
    }))
    return true
  } catch (error) {
    console.error('保存游戏配置失败:', error)
    return false
  }
}

// 获取特定级别的背景颜色
export function getLevelColor(level) {
  const config = getGameConfig()
  return config.levelColors[`level${level}`] || DEFAULT_CONFIG.levelColors[`level${level}`]
}

// 获取英文字体大小
export function getEnglishFontSize() {
  const config = getGameConfig()
  return config.englishFontSize || DEFAULT_CONFIG.englishFontSize
}

// 获取中文字体大小
export function getChineseFontSize() {
  const config = getGameConfig()
  return config.chineseFontSize || DEFAULT_CONFIG.chineseFontSize
}

// 监听配置更新
export function onConfigUpdate(callback) {
  window.addEventListener('gameConfigUpdated', (event) => {
    callback(event.detail)
  })
}

// 移除配置更新监听
export function offConfigUpdate(callback) {
  window.removeEventListener('gameConfigUpdated', callback)
}