/**
 * 词库管理API工具类
 */
import { apiClient } from '@/utils/api.js'

export const vocabularyApi = {
  // ==================== 词库管理 ====================
  
  /**
   * 获取词库列表
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getLibraries(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `/vocabulary-test/libraries?${queryString}` : '/vocabulary-test/libraries'
    return apiClient.get(url)
  },

  /**
   * 创建词库
   * @param {Object} data - 词库数据
   * @returns {Promise}
   */
  createLibrary(data) {
    return apiClient.post('/vocabulary-test/libraries', data)
  },

  /**
   * 获取词库详情
   * @param {number} libraryId - 词库ID
   * @returns {Promise}
   */
  getLibrary(libraryId) {
    return apiClient.get(`/vocabulary-test/libraries/${libraryId}`)
  },

  /**
   * 更新词库
   * @param {number} libraryId - 词库ID
   * @param {Object} data - 更新数据
   * @returns {Promise}
   */
  updateLibrary(libraryId, data) {
    return apiClient.put(`/vocabulary-test/libraries/${libraryId}`, data)
  },

  /**
   * 删除词库
   * @param {number} libraryId - 词库ID
   * @returns {Promise}
   */
  deleteLibrary(libraryId) {
    return apiClient.delete(`/vocabulary-test/libraries/${libraryId}`)
  },

  // ==================== 词组管理 ====================

  /**
   * 获取词组列表
   * @param {number} libraryId - 词库ID
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getGroups(libraryId, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? 
      `/vocabulary-test/libraries/${libraryId}/groups?${queryString}` : 
      `/vocabulary-test/libraries/${libraryId}/groups`
    return apiClient.get(url)
  },

  /**
   * 创建词组
   * @param {number} libraryId - 词库ID
   * @param {Object} data - 词组数据
   * @returns {Promise}
   */
  createGroup(libraryId, data) {
    return apiClient.post(`/vocabulary-test/libraries/${libraryId}/groups`, data)
  },

  /**
   * 获取词组详情
   * @param {number} groupId - 词组ID
   * @returns {Promise}
   */
  getGroup(groupId) {
    return apiClient.get(`/vocabulary-test/groups/${groupId}`)
  },

  /**
   * 更新词组
   * @param {number} groupId - 词组ID
   * @param {Object} data - 更新数据
   * @returns {Promise}
   */
  updateGroup(groupId, data) {
    return apiClient.put(`/vocabulary-test/groups/${groupId}`, data)
  },

  /**
   * 删除词组
   * @param {number} groupId - 词组ID
   * @returns {Promise}
   */
  deleteGroup(groupId) {
    return apiClient.delete(`/vocabulary-test/groups/${groupId}`)
  },

  // ==================== 单词管理 ====================

  /**
   * 获取单词列表
   * @param {number} groupId - 词组ID
   * @param {Object} params - 查询参数
   * @returns {Promise}
   */
  getWords(groupId, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? 
      `/vocabulary-test/groups/${groupId}/words?${queryString}` : 
      `/vocabulary-test/groups/${groupId}/words`
    return apiClient.get(url)
  },

  /**
   * 创建单词
   * @param {number} groupId - 词组ID
   * @param {Object} data - 单词数据
   * @returns {Promise}
   */
  createWord(groupId, data) {
    return apiClient.post(`/vocabulary-test/groups/${groupId}/words`, data)
  },

  /**
   * 获取单词详情
   * @param {number} wordId - 单词ID
   * @returns {Promise}
   */
  getWord(wordId) {
    return apiClient.get(`/vocabulary-test/words/${wordId}`)
  },

  /**
   * 更新单词
   * @param {number} wordId - 单词ID
   * @param {Object} data - 更新数据
   * @returns {Promise}
   */
  updateWord(wordId, data) {
    return apiClient.put(`/vocabulary-test/words/${wordId}`, data)
  },

  /**
   * 删除单词
   * @param {number} wordId - 单词ID
   * @returns {Promise}
   */
  deleteWord(wordId) {
    return apiClient.delete(`/vocabulary-test/words/${wordId}`)
  },

  /**
   * 批量导入单词
   * @param {number} groupId - 词组ID
   * @param {Array} words - 单词数据数组
   * @returns {Promise}
   */
  batchImportWords(groupId, words) {
    return apiClient.post(`/vocabulary-test/groups/${groupId}/words/batch`, { words })
  },

  // ==================== 搜索功能 ====================

  /**
   * 搜索词库
   * @param {string} query - 搜索关键词
   * @param {Object} filters - 筛选条件
   * @returns {Promise}
   */
  searchLibraries(query, filters = {}) {
    const params = { search: query, ...filters }
    return this.getLibraries(params)
  },

  /**
   * 搜索单词
   * @param {string} query - 搜索关键词
   * @param {Object} filters - 筛选条件
   * @returns {Promise}
   */
  searchWords(query, filters = {}) {
    const params = { search: query, ...filters }
    return apiClient.get(`/vocabulary-test/words/search?${new URLSearchParams(params).toString()}`)
  }
}