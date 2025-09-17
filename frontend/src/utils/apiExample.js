/**
 * API 使用示例
 * 展示如何在 Vue 组件中使用 API 客户端
 */

import { apiClient } from './api.js'

// 示例：用户相关 API
export const userApi = {
  // 获取用户列表
  async getUsers() {
    return await apiClient.get('/users')
  },

  // 获取单个用户
  async getUser(id) {
    return await apiClient.get(`/users/${id}`)
  },

  // 创建用户
  async createUser(userData) {
    return await apiClient.post('/users', userData)
  },

  // 更新用户
  async updateUser(id, userData) {
    return await apiClient.put(`/users/${id}`, userData)
  },

  // 删除用户
  async deleteUser(id) {
    return await apiClient.delete(`/users/${id}`)
  }
}

// 示例：单词相关 API（根据项目名称推测）
export const wordApi = {
  // 获取单词列表
  async getWords(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `/words?${queryString}` : '/words'
    return await apiClient.get(url)
  },

  // 搜索单词
  async searchWords(keyword) {
    return await apiClient.get(`/words/search?q=${encodeURIComponent(keyword)}`)
  },

  // 获取单词详情
  async getWordDetail(id) {
    return await apiClient.get(`/words/${id}`)
  },

  // 添加单词
  async addWord(wordData) {
    return await apiClient.post('/words', wordData)
  },

  // 更新单词
  async updateWord(id, wordData) {
    return await apiClient.put(`/words/${id}`, wordData)
  },

  // 删除单词
  async deleteWord(id) {
    return await apiClient.delete(`/words/${id}`)
  },

  // 单词爆炸分析
  async explodeWord(word) {
    return await apiClient.post('/words/explode', { word })
  }
}

// 示例：认证相关 API
export const authApi = {
  // 用户登录
  async login(credentials) {
    return await apiClient.post('/auth/login', credentials)
  },

  // 用户注册
  async register(userData) {
    return await apiClient.post('/auth/register', userData)
  },

  // 获取当前用户信息
  async getCurrentUser() {
    return await apiClient.get('/auth/me')
  },

  // 刷新令牌
  async refreshToken() {
    return await apiClient.post('/auth/refresh')
  },

  // 用户登出
  async logout() {
    return await apiClient.post('/auth/logout')
  }
}

// Vue 组件中的使用示例
export const componentExample = `
<template>
  <div>
    <h2>单词列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else>
      <li v-for="word in words" :key="word.id">
        {{ word.name }} - {{ word.meaning }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { wordApi } from '@/utils/apiExample.js'

export default {
  name: 'WordList',
  setup() {
    const words = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchWords = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await wordApi.getWords()
        words.value = response.data || response
      } catch (err) {
        error.value = err.message || '获取单词列表失败'
        console.error('获取单词列表失败:', err)
      } finally {
        loading.value = false
      }
    }

    const explodeWord = async (word) => {
      try {
        const result = await wordApi.explodeWord(word)
        console.log('单词爆炸结果:', result)
        return result
      } catch (err) {
        console.error('单词爆炸失败:', err)
        throw err
      }
    }

    onMounted(() => {
      fetchWords()
    })

    return {
      words,
      loading,
      error,
      fetchWords,
      explodeWord
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
  padding: 10px;
  background-color: #ffe6e6;
  border: 1px solid #ff9999;
  border-radius: 4px;
}
</style>
`