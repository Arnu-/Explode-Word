/**
 * 用户服务 - 处理用户相关的API调用
 */
import { apiClient } from '@/utils/api.js'

class UserService {
  /**
   * 获取用户完整档案信息
   */
  async getUserProfile() {
    try {
      const response = await apiClient.get('/users/profile')
      return response
    } catch (error) {
      console.error('获取用户档案失败:', error)
      throw error
    }
  }

  /**
   * 更新用户档案信息
   * @param {Object} profileData - 用户档案数据
   */
  async updateUserProfile(profileData) {
    try {
      const response = await apiClient.put('/users/profile', profileData)
      return response
    } catch (error) {
      console.error('更新用户档案失败:', error)
      throw error
    }
  }

  /**
   * 获取用户统计信息
   */
  async getUserStats() {
    try {
      const response = await apiClient.get('/users/stats')
      return response
    } catch (error) {
      console.error('获取用户统计失败:', error)
      throw error
    }
  }

  /**
   * 获取排行榜
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 限制数量
   * @param {string} params.sort_by - 排序方式 (best_score, total_wins, win_rate)
   */
  async getLeaderboard(params = {}) {
    try {
      const response = await apiClient.get('/users/leaderboard', { params })
      return response
    } catch (error) {
      console.error('获取排行榜失败:', error)
      throw error
    }
  }

  /**
   * 搜索用户
   * @param {string} query - 搜索关键词
   * @param {number} limit - 限制数量
   */
  async searchUsers(query, limit = 20) {
    try {
      const response = await apiClient.get('/users/search', {
        params: { q: query, limit }
      })
      return response
    } catch (error) {
      console.error('搜索用户失败:', error)
      throw error
    }
  }

  /**
   * 获取指定用户的公开信息
   * @param {number} userId - 用户ID
   */
  async getUserInfo(userId) {
    try {
      const response = await apiClient.get(`/users/${userId}`)
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  /**
   * 格式化用户档案数据以匹配前端组件需求
   * @param {Object} profileData - 后端返回的档案数据
   */
  formatProfileForUI(profileData) {
    if (!profileData) {
      console.warn('formatProfileForUI: profileData为空');
      return this.getDefaultProfile();
    }

    const { user_info, game_history, achievements, statistics } = profileData;

    return {
      userInfo: {
        username: user_info?.username || '游客',
        email: user_info?.email || '',
        level: user_info?.level || 1,
        coins: user_info?.coins || 0,
        completedLevels: user_info?.completedLevels || 0,
        totalStars: user_info?.totalStars || 0,
        totalPlayTime: user_info?.totalPlayTime || '0m',
        accuracy: user_info?.accuracy || '0%',
        streak: user_info?.streak || 0,
        createdAt: user_info?.created_at ? new Date(user_info.created_at) : new Date()
      },
      gameHistory: this.formatGameHistory(game_history || []),
      achievements: achievements || [],
      statistics: {
        weeklyGames: statistics?.weekly_games || 0,
        averageScore: statistics?.average_score || 0,
        totalTimePlayed: statistics?.total_time_played || 0,
        totalCorrectAnswers: statistics?.total_correct_answers || 0,
        totalWrongAnswers: statistics?.total_wrong_answers || 0
      }
    };
  }

  /**
   * 格式化游戏历史记录
   * @param {Array} gameHistory - 游戏历史数据
   */
  formatGameHistory(gameHistory) {
    return gameHistory.map(game => ({
      id: game.id,
      levelId: game.levelId,
      levelName: game.levelName,
      mode: game.mode,
      score: game.score,
      duration: game.duration,
      accuracy: game.accuracy,
      result: game.result,
      stars: game.stars,
      playedAt: game.playedAt ? new Date(game.playedAt) : new Date()
    }));
  }

  /**
   * 获取默认档案数据（用于错误情况）
   */
  getDefaultProfile() {
    return {
      userInfo: {
        username: '游客',
        email: '',
        level: 1,
        coins: 0,
        completedLevels: 0,
        totalStars: 0,
        totalPlayTime: '0m',
        accuracy: '0%',
        streak: 0,
        createdAt: new Date()
      },
      gameHistory: [],
      achievements: [
        {
          id: 1,
          name: '初出茅庐',
          description: '完成第一个关卡',
          icon: 'fa-solid fa-star',
          unlocked: false
        },
        {
          id: 2,
          name: '词汇达人',
          description: '学会100个单词',
          icon: 'fa-solid fa-book',
          unlocked: false
        },
        {
          id: 3,
          name: '连胜王者',
          description: '连续7天游戏',
          icon: 'fa-solid fa-fire',
          unlocked: false
        },
        {
          id: 4,
          name: '完美主义',
          description: '单关卡100%正确率',
          icon: 'fa-solid fa-bullseye',
          unlocked: false
        },
        {
          id: 5,
          name: '时间管理',
          description: '在限定时间内完成关卡',
          icon: 'fa-solid fa-stopwatch',
          unlocked: false
        },
        {
          id: 6,
          name: '收藏家',
          description: '收集所有星星',
          icon: 'fa-solid fa-gem',
          unlocked: false
        }
      ],
      statistics: {
        weeklyGames: 0,
        averageScore: 0,
        totalTimePlayed: 0,
        totalCorrectAnswers: 0,
        totalWrongAnswers: 0
      }
    };
  }
}

export default new UserService()