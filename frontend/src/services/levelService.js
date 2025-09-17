/**
 * 关卡服务 - 处理关卡相关的API调用
 */
import { apiClient } from '@/utils/api.js'

class LevelService {
  /**
   * 获取关卡列表（包含用户记录）
   */
  async getLevels() {
    try {
      const response = await apiClient.get('/levels/')
      console.log('关卡API原始响应:', response);
      return response
    } catch (error) {
      console.error('获取关卡列表失败:', error)
      throw error
    }
  }

  /**
   * 获取关卡详情
   * @param {number} levelId - 关卡ID
   */
  async getLevelDetail(levelId) {
    try {
      const response = await apiClient.get(`/levels/${levelId}`)
      return response
    } catch (error) {
      console.error('获取关卡详情失败:', error)
      throw error
    }
  }

  /**
   * 开始关卡游戏
   * @param {number} levelId - 关卡ID
   */
  async startLevel(levelId) {
    try {
      const response = await apiClient.post(`/levels/${levelId}/start`)
      return response
    } catch (error) {
      console.error('开始关卡失败:', error)
      throw error
    }
  }

  /**
   * 完成关卡
   * @param {number} levelId - 关卡ID
   * @param {Object} gameResult - 游戏结果
   * @param {number} gameResult.score - 得分
   * @param {number} gameResult.time_seconds - 用时（秒）
   * @param {number} gameResult.correct_answers - 正确答案数
   * @param {number} gameResult.wrong_answers - 错误答案数
   * @param {Array} gameResult.tasks_result - 任务完成结果
   */
  async completeLevel(levelId, gameResult) {
    try {
      const response = await apiClient.post(`/levels/${levelId}/complete`, gameResult)
      return response
    } catch (error) {
      console.error('完成关卡失败:', error)
      throw error
    }
  }

  /**
   * 获取游戏历史记录
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.per_page - 每页数量
   * @param {number} params.level_id - 关卡ID（可选）
   */
  async getGameHistory(params = {}) {
    try {
      const response = await apiClient.get('/levels/history', { params })
      return response
    } catch (error) {
      console.error('获取游戏历史失败:', error)
      throw error
    }
  }

  /**
   * 获取用户游戏进度
   */
  async getUserProgress() {
    try {
      const response = await apiClient.get('/levels/progress')
      console.log('进度API原始响应:', response);
      return response
    } catch (error) {
      console.error('获取用户进度失败:', error)
      throw error
    }
  }

  /**
   * 创建关卡（管理员功能）
   * @param {Object} levelData - 关卡数据
   */
  async createLevel(levelData) {
    try {
      const response = await apiClient.post('/levels/admin/levels', levelData)
      return response
    } catch (error) {
      console.error('创建关卡失败:', error)
      throw error
    }
  }

  /**
   * 格式化关卡数据以匹配前端组件需求
   * @param {Array} levels - 后端返回的关卡数据
   */
  formatLevelsForUI(levels) {
    if (!Array.isArray(levels)) {
      console.warn('formatLevelsForUI: levels不是数组', levels);
      return [];
    }
    
    return levels.map(level => {
      console.log('格式化关卡数据:', level);
      return {
        id: level.id,
        title: level.title,
        difficulty: level.difficulty,
        status: level.status,
        stars: level.stars || 0,
        estTimeMin: level.estimated_time_minutes || level.estTimeMin || 0,
        tasks: level.tasks || [],
        bestScore: level.best_score,
        lastPlayedAgo: level.last_played_ago || level.lastPlayedAgo || '—',
        rewardCoin: level.reward_coins || level.rewardCoin || 0,
        totalAttempts: level.total_attempts || 0,
        completedAttempts: level.completed_attempts || 0,
        completionRate: level.completion_rate || 0
      };
    });
  }

  /**
   * 模拟游戏数据（用于测试）
   */
  getMockLevels() {
    return [
      {
        id: 1,
        title: '魔法森林挑战',
        difficulty: '简单',
        status: 'completed',
        stars: 3,
        estTimeMin: 6,
        tasks: [
          { text: '收集至少15个魔法宝石', done: true },
          { text: '在60秒内完成关卡', done: false },
          { text: '不损失任何生命值', done: true }
        ],
        bestScore: 12450,
        lastPlayedAgo: '2天前',
        rewardCoin: 12450
      },
      {
        id: 2,
        title: '魔法森林挑战',
        difficulty: '简单',
        status: 'completed',
        stars: 2,
        estTimeMin: 6,
        tasks: [
          { text: '收集至少10个魔法宝石', done: true },
          { text: '在90秒内完成关卡', done: true },
          { text: '不损失任何生命值', done: false }
        ],
        bestScore: 9820,
        lastPlayedAgo: '5天前',
        rewardCoin: 10800
      },
      {
        id: 3,
        title: '魔法森林挑战',
        difficulty: '中等',
        status: 'available',
        stars: 1,
        estTimeMin: 7,
        tasks: [
          { text: '收集至少20个魔法宝石', done: true },
          { text: '在120秒内完成关卡', done: false },
          { text: '不损失任何生命值', done: false }
        ],
        bestScore: 7650,
        lastPlayedAgo: '7天前',
        rewardCoin: 11500
      },
      {
        id: 4,
        title: '魔法森林挑战',
        difficulty: '中等',
        status: 'available',
        stars: 0,
        estTimeMin: 8,
        tasks: [
          { text: '收集至少25个魔法宝石', done: false },
          { text: '在150秒内完成关卡', done: false },
          { text: '不损失任何生命值', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 12450
      },
      {
        id: 5,
        title: '魔法森林挑战',
        difficulty: '中等',
        status: 'available',
        stars: 0,
        estTimeMin: 8,
        tasks: [
          { text: '收集至少30个魔法宝石', done: false },
          { text: '在180秒内完成关卡', done: false },
          { text: '不损失任何生命值', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 12450
      },
      {
        id: 6,
        title: '魔法森林挑战',
        difficulty: '困难',
        status: 'available',
        stars: 0,
        estTimeMin: 9,
        tasks: [
          { text: '收集至少35个魔法宝石', done: false },
          { text: '在210秒内完成关卡', done: false },
          { text: '不损失任何生命值', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 14800
      },
      {
        id: 7,
        title: '魔法森林挑战',
        difficulty: '未知',
        status: 'locked',
        stars: 0,
        estTimeMin: 9,
        tasks: [
          { text: '???', done: false },
          { text: '???', done: false },
          { text: '???', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 16000
      },
      {
        id: 8,
        title: '魔法森林挑战',
        difficulty: '未知',
        status: 'locked',
        stars: 0,
        estTimeMin: 9,
        tasks: [
          { text: '???', done: false },
          { text: '???', done: false },
          { text: '???', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 16000
      },
      {
        id: 9,
        title: '待开放',
        difficulty: '未知',
        status: 'coming-soon',
        stars: 0,
        estTimeMin: 0,
        tasks: [
          { text: '敬请期待', done: false },
          { text: '敬请期待', done: false },
          { text: '敬请期待', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: 0
      }
    ]
  }
}

export default new LevelService()