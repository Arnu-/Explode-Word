/**
 * 词库游戏服务 - 处理基于词库的游戏API调用
 */
import { apiClient } from '@/utils/api.js'

class VocabularyGameService {
  /**
   * 开始词库游戏
   * @param {number} libraryId - 词库ID
   * @param {number} groupId - 词组ID
   */
  async startGame(libraryId, groupId) {
    try {
      const response = await apiClient.post('/vocabulary-game/start', {
        library_id: libraryId,
        group_id: groupId
      })
      return response
    } catch (error) {
      console.error('开始词库游戏失败:', error)
      throw error
    }
  }

  /**
   * 获取游戏单词数据
   * @param {string} sessionCode - 游戏会话代码
   */
  async getGameWords(sessionCode) {
    try {
      const response = await apiClient.get(`/vocabulary-game/${sessionCode}/words`)
      return response
    } catch (error) {
      console.error('获取游戏单词失败:', error)
      throw error
    }
  }

  /**
   * 提交答案
   * @param {string} sessionCode - 游戏会话代码
   * @param {Object} answerData - 答案数据
   */
  async submitAnswer(sessionCode, answerData) {
    try {
      const response = await apiClient.post(`/vocabulary-game/${sessionCode}/answer`, answerData)
      return response
    } catch (error) {
      console.error('提交答案失败:', error)
      throw error
    }
  }

  /**
   * 结束游戏
   * @param {string} sessionCode - 游戏会话代码
   */
  async finishGame(sessionCode) {
    try {
      const response = await apiClient.post(`/vocabulary-game/${sessionCode}/finish`)
      return response
    } catch (error) {
      console.error('结束游戏失败:', error)
      throw error
    }
  }

  /**
   * 获取游戏状态
   * @param {string} sessionCode - 游戏会话代码
   */
  async getGameStatus(sessionCode) {
    try {
      const response = await apiClient.get(`/vocabulary-game/${sessionCode}/status`)
      return response
    } catch (error) {
      console.error('获取游戏状态失败:', error)
      throw error
    }
  }
}

export default new VocabularyGameService()