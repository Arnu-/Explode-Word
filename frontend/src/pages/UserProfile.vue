<template>
  <div class="profile-page">
    <div class="page-overlay"></div>
    
    <div class="profile-container content-layer">
      <div class="profile-header">
        <div class="avatar-section">
          <div class="user-avatar-large">
            <i class="fa-solid fa-user"></i>
          </div>
          <button class="change-avatar-btn">
            <i class="fa-solid fa-camera"></i>
            更换头像
          </button>
        </div>
        
        <div class="user-info">
          <h1 class="username">{{ userInfo.username || '游客' }}</h1>
          <div class="user-stats">
            <div class="stat-item">
              <div class="stat-value">{{ userInfo.level || 42 }}</div>
              <div class="stat-label">等级</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ (userInfo.coins || 3250).toLocaleString() }}</div>
              <div class="stat-label">金币</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userInfo.completedLevels || 28 }}</div>
              <div class="stat-label">完成关卡</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="profile-content">
        <!-- 个人信息 -->
        <div class="info-section">
          <h3 class="section-title">个人信息</h3>
          <div class="info-form">
            <div class="form-group">
              <label class="form-label">用户名</label>
              <input 
                type="text" 
                v-model="editableInfo.username" 
                class="form-input"
                :disabled="!isEditing"
              >
            </div>
            <div class="form-group">
              <label class="form-label">邮箱</label>
              <input 
                type="email" 
                v-model="editableInfo.email" 
                class="form-input"
                :disabled="!isEditing"
              >
            </div>
            <div class="form-group">
              <label class="form-label">注册时间</label>
              <input 
                type="text" 
                :value="formatDate(userInfo.createdAt)" 
                class="form-input"
                disabled
              >
            </div>
          </div>
          
          <div class="form-actions">
            <button v-if="!isEditing" @click="startEditing" class="edit-btn">
              <i class="fa-solid fa-pen"></i>
              编辑信息
            </button>
            <template v-else>
              <button @click="cancelEditing" class="cancel-btn">
                <i class="fa-solid fa-times"></i>
                取消
              </button>
              <button @click="saveProfile" class="save-btn">
                <i class="fa-solid fa-check"></i>
                保存
              </button>
            </template>
          </div>
        </div>
        
        <!-- 游戏统计 -->
        <div class="stats-section">
          <h3 class="section-title">游戏统计</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fa-solid fa-trophy"></i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ userInfo.totalStars || 156 }}</div>
                <div class="stat-text">获得星星</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fa-solid fa-clock"></i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ userInfo.totalPlayTime || '24h' }}</div>
                <div class="stat-text">游戏时长</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fa-solid fa-target"></i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ userInfo.accuracy || '89%' }}</div>
                <div class="stat-text">平均准确率</div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fa-solid fa-fire"></i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ userInfo.streak || 7 }}</div>
                <div class="stat-text">连胜天数</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 游戏历史记录 -->
        <div class="game-history-section">
          <h3 class="section-title">游戏历史记录</h3>
          <div class="history-controls">
            <div class="filter-tabs">
              <button 
                v-for="filter in historyFilters" 
                :key="filter.key"
                @click="currentHistoryFilter = filter.key"
                class="filter-tab"
                :class="{ active: currentHistoryFilter === filter.key }"
              >
                {{ filter.label }}
              </button>
            </div>
            <div class="history-stats">
              <div class="quick-stat">
                <span class="stat-label">本周游戏：</span>
                <span class="stat-value">{{ weeklyGames }}</span>
              </div>
              <div class="quick-stat">
                <span class="stat-label">平均分数：</span>
                <span class="stat-value">{{ averageScore }}</span>
              </div>
            </div>
          </div>
          
          <div class="game-history-list">
            <div 
              v-for="game in filteredGameHistory" 
              :key="game.id"
              class="history-item"
            >
              <div class="game-info">
                <div class="game-level">
                  <i class="fa-solid fa-gamepad"></i>
                  {{ game.levelName }}
                </div>
                <div class="game-mode">{{ game.mode }}</div>
              </div>
              
              <div class="game-stats">
                <div class="stat-group">
                  <div class="stat-item">
                    <span class="stat-label">分数</span>
                    <span class="stat-value" :class="getScoreClass(game.score)">{{ game.score }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">用时</span>
                    <span class="stat-value">{{ formatGameTime(game.duration) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">准确率</span>
                    <span class="stat-value" :class="getAccuracyClass(game.accuracy)">{{ game.accuracy }}%</span>
                  </div>
                </div>
                
                <div class="game-result">
                  <div class="result-badge" :class="game.result">
                    <i :class="getResultIcon(game.result)"></i>
                    {{ getResultText(game.result) }}
                  </div>
                  <div class="stars-earned">
                    <i 
                      v-for="star in 3" 
                      :key="star"
                      class="fa-solid fa-star"
                      :class="{ earned: star <= game.stars }"
                    ></i>
                  </div>
                </div>
              </div>
              
              <div class="game-meta">
                <div class="play-date">{{ formatDate(game.playedAt) }}</div>
                <button class="replay-btn" @click="replayLevel(game.levelId)">
                  <i class="fa-solid fa-redo"></i>
                  重玩
                </button>
              </div>
            </div>
          </div>
          
          <div v-if="filteredGameHistory.length === 0" class="empty-history">
            <i class="fa-solid fa-history"></i>
            <p>暂无游戏记录</p>
            <button @click="$router.push({ name: 'wordblast' })" class="start-game-btn">
              开始第一局游戏
            </button>
          </div>
        </div>

        <!-- 成就系统 -->
        <div class="achievements-section">
          <h3 class="section-title">成就徽章</h3>
          <div class="achievements-grid">
            <div 
              v-for="achievement in achievements" 
              :key="achievement.id"
              class="achievement-card"
              :class="{ unlocked: achievement.unlocked }"
            >
              <div class="achievement-icon">
                <i :class="achievement.icon"></i>
              </div>
              <div class="achievement-info">
                <div class="achievement-name">{{ achievement.name }}</div>
                <div class="achievement-desc">{{ achievement.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/utils/auth.js'
import { useRouter } from 'vue-router'

const { currentUser } = useAuth()
const router = useRouter()

// 用户信息
const userInfo = ref({
  username: '单词大师',
  email: 'user@example.com',
  level: 42,
  coins: 3250,
  completedLevels: 28,
  totalStars: 156,
  totalPlayTime: '24h',
  accuracy: '89%',
  streak: 7,
  createdAt: new Date('2023-01-15')
})

// 可编辑的用户信息
const editableInfo = ref({})
const isEditing = ref(false)

// 游戏历史记录
const gameHistory = ref([
  {
    id: 1,
    levelId: 1,
    levelName: '第一关：小试牛刀',
    mode: '训练模式',
    score: 450,
    duration: 180, // 秒
    accuracy: 92,
    result: 'success', // success, failed, perfect
    stars: 3,
    playedAt: new Date('2024-01-15T10:30:00')
  },
  {
    id: 2,
    levelId: 2,
    levelName: '第二关：词汇进阶',
    mode: '挑战模式',
    score: 380,
    duration: 240,
    accuracy: 85,
    result: 'success',
    stars: 2,
    playedAt: new Date('2024-01-15T14:20:00')
  },
  {
    id: 3,
    levelId: 1,
    levelName: '第一关：小试牛刀',
    mode: '挑战模式',
    score: 520,
    duration: 150,
    accuracy: 98,
    result: 'perfect',
    stars: 3,
    playedAt: new Date('2024-01-14T16:45:00')
  },
  {
    id: 4,
    levelId: 3,
    levelName: '第三关：高级挑战',
    mode: '训练模式',
    score: 280,
    duration: 300,
    accuracy: 75,
    result: 'failed',
    stars: 1,
    playedAt: new Date('2024-01-14T09:15:00')
  },
  {
    id: 5,
    levelId: 2,
    levelName: '第二关：词汇进阶',
    mode: '训练模式',
    score: 420,
    duration: 200,
    accuracy: 88,
    result: 'success',
    stars: 2,
    playedAt: new Date('2024-01-13T20:30:00')
  }
])

// 历史记录筛选
const historyFilters = ref([
  { key: 'all', label: '全部' },
  { key: 'today', label: '今天' },
  { key: 'week', label: '本周' },
  { key: 'month', label: '本月' }
])

const currentHistoryFilter = ref('all')

// 计算属性
const filteredGameHistory = computed(() => {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const weekStart = new Date(today.getTime() - (today.getDay() * 24 * 60 * 60 * 1000))
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)

  return gameHistory.value.filter(game => {
    const gameDate = new Date(game.playedAt)
    
    switch (currentHistoryFilter.value) {
      case 'today':
        return gameDate >= today
      case 'week':
        return gameDate >= weekStart
      case 'month':
        return gameDate >= monthStart
      default:
        return true
    }
  }).sort((a, b) => new Date(b.playedAt) - new Date(a.playedAt))
})

const weeklyGames = computed(() => {
  const now = new Date()
  const weekStart = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
  return gameHistory.value.filter(game => new Date(game.playedAt) >= weekStart).length
})

const averageScore = computed(() => {
  if (gameHistory.value.length === 0) return 0
  const total = gameHistory.value.reduce((sum, game) => sum + game.score, 0)
  return Math.round(total / gameHistory.value.length)
})

// 成就数据
const achievements = ref([
  {
    id: 1,
    name: '初出茅庐',
    description: '完成第一个关卡',
    icon: 'fa-solid fa-star',
    unlocked: true
  },
  {
    id: 2,
    name: '词汇达人',
    description: '学会100个单词',
    icon: 'fa-solid fa-book',
    unlocked: true
  },
  {
    id: 3,
    name: '连胜王者',
    description: '连续7天游戏',
    icon: 'fa-solid fa-fire',
    unlocked: true
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
])

// 开始编辑
const startEditing = () => {
  editableInfo.value = { ...userInfo.value }
  isEditing.value = true
}

// 取消编辑
const cancelEditing = () => {
  editableInfo.value = {}
  isEditing.value = false
}

// 保存个人资料
const saveProfile = async () => {
  try {
    // 这里应该调用API保存用户信息
    userInfo.value = { ...userInfo.value, ...editableInfo.value }
    isEditing.value = false
    console.log('个人资料已保存')
  } catch (error) {
    console.error('保存个人资料失败:', error)
  }
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '未知'
  const gameDate = new Date(date)
  const now = new Date()
  const diffTime = now - gameDate
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return '今天 ' + gameDate.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (diffDays === 1) {
    return '昨天 ' + gameDate.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else {
    return gameDate.toLocaleDateString('zh-CN')
  }
}

// 格式化游戏时长
const formatGameTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 获取分数样式类
const getScoreClass = (score) => {
  if (score >= 500) return 'score-excellent'
  if (score >= 400) return 'score-good'
  if (score >= 300) return 'score-average'
  return 'score-poor'
}

// 获取准确率样式类
const getAccuracyClass = (accuracy) => {
  if (accuracy >= 95) return 'accuracy-excellent'
  if (accuracy >= 85) return 'accuracy-good'
  if (accuracy >= 75) return 'accuracy-average'
  return 'accuracy-poor'
}

// 获取结果图标
const getResultIcon = (result) => {
  switch (result) {
    case 'perfect': return 'fa-solid fa-crown'
    case 'success': return 'fa-solid fa-check-circle'
    case 'failed': return 'fa-solid fa-times-circle'
    default: return 'fa-solid fa-question-circle'
  }
}

// 获取结果文本
const getResultText = (result) => {
  switch (result) {
    case 'perfect': return '完美'
    case 'success': return '成功'
    case 'failed': return '失败'
    default: return '未知'
  }
}

// 重玩关卡
const replayLevel = (levelId) => {
  router.push({ name: 'game', params: { levelId } })
}

// 加载用户数据
const loadUserData = () => {
  if (currentUser.value) {
    userInfo.value = {
      ...userInfo.value,
      ...currentUser.value
    }
  }
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
@import '@/assets/theme.css';

.profile-page {
  min-height: 100vh;
  color: var(--color-text-primary);
  position: relative;
  padding: 2rem;
  overflow: hidden;
}

.page-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
  z-index: 0;
  border-radius: var(--border-radius-large);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.1);
}

.content-layer {
  position: relative;
  z-index: 1;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 3rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.user-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa 0%, #6366f1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
  box-shadow: 0 8px 32px rgba(96, 165, 250, 0.3);
}

.change-avatar-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.change-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.user-info {
  flex: 1;
}

.username {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
}

.stat-label {
  font-size: 0.875rem;
  color: #cbd5e1;
  margin-top: 0.25rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-section, .stats-section, .achievements-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
}

.info-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.form-input {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  color: white;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.edit-btn, .cancel-btn, .save-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.cancel-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.save-btn {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.edit-btn:hover, .save-btn:hover {
  transform: translateY(-2px);
}

.cancel-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-medium);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
}

.stat-text {
  font-size: 0.875rem;
  color: #cbd5e1;
}

/* 游戏历史记录样式 */
.game-history-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.history-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.filter-tab {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  color: #cbd5e1;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.15);
}

.filter-tab.active {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border-color: #3b82f6;
}

.history-stats {
  display: flex;
  gap: 2rem;
}

.quick-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.quick-stat .stat-label {
  color: #cbd5e1;
}

.quick-stat .stat-value {
  color: #ffffff;
  font-weight: 600;
}

.game-history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-medium);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.game-info {
  flex: 1;
  min-width: 0;
}

.game-level {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.game-mode {
  font-size: 0.875rem;
  color: #cbd5e1;
}

.game-stats {
  display: flex;
  align-items: center;
  gap: 2rem;
  flex: 2;
}

.stat-group {
  display: flex;
  gap: 1.5rem;
}

.stat-group .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-group .stat-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-group .stat-value {
  font-size: 1rem;
  font-weight: 600;
}

/* 分数颜色 */
.score-excellent { color: #22c55e; }
.score-good { color: #3b82f6; }
.score-average { color: #f59e0b; }
.score-poor { color: #ef4444; }

/* 准确率颜色 */
.accuracy-excellent { color: #22c55e; }
.accuracy-good { color: #3b82f6; }
.accuracy-average { color: #f59e0b; }
.accuracy-poor { color: #ef4444; }

.game-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.result-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.result-badge.perfect {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

.result-badge.success {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.result-badge.failed {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.stars-earned {
  display: flex;
  gap: 0.125rem;
}

.stars-earned .fa-star {
  font-size: 0.875rem;
  color: #64748b;
}

.stars-earned .fa-star.earned {
  color: #fbbf24;
}

.game-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex: 1;
  min-width: 0;
}

.play-date {
  font-size: 0.75rem;
  color: #94a3b8;
  white-space: nowrap;
}

.replay-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 0.375rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
}

.replay-btn:hover {
  background: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}

.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  color: #94a3b8;
}

.empty-history i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-history p {
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.start-game-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.start-game-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.achievement-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-medium);
  border: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0.5;
  transition: all 0.3s;
}

.achievement-card.unlocked {
  opacity: 1;
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.3);
}

.achievement-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}

.achievement-name {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

.achievement-desc {
  font-size: 0.875rem;
  color: #cbd5e1;
  margin-top: 0.25rem;
}

@media (max-width: 768px) {
  .profile-page {
    padding: 1rem;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  /* 游戏历史记录响应式 */
  .history-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .history-stats {
    justify-content: space-around;
  }
  
  .history-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .game-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .stat-group {
    justify-content: space-around;
  }
  
  .game-meta {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .filter-tabs {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
  
  .history-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .stat-group {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .stat-group .stat-item {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>