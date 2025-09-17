<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">爆炸单词 - 仪表板</h1>
        <div class="user-info">
          <span class="welcome-text">欢迎, {{ user?.nickname || user?.username }}</span>
          <button @click="handleLogout" class="logout-button">退出登录</button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="dashboard-content">
        <!-- 用户统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">🎮</div>
            <div class="stat-info">
              <h3>总游戏数</h3>
              <p class="stat-value">{{ user?.total_games || 0 }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-info">
              <h3>胜利次数</h3>
              <p class="stat-value">{{ user?.total_wins || 0 }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3>胜率</h3>
              <p class="stat-value">{{ user?.win_rate || 0 }}%</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">⭐</div>
            <div class="stat-info">
              <h3>最高分</h3>
              <p class="stat-value">{{ user?.best_score || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions">
          <h2>快速开始</h2>
          <div class="action-grid">
            <router-link to="/game" class="action-card">
              <div class="action-icon">🎯</div>
              <h3>开始游戏</h3>
              <p>立即开始一局爆炸单词游戏</p>
            </router-link>
            
            <router-link to="/levels" class="action-card">
              <div class="action-icon">📚</div>
              <h3>选择关卡</h3>
              <p>浏览和选择不同难度的关卡</p>
            </router-link>
            
            <router-link to="/profile" class="action-card">
              <div class="action-icon">👤</div>
              <h3>个人资料</h3>
              <p>查看和编辑个人信息</p>
            </router-link>
            
            <router-link to="/leaderboard" class="action-card">
              <div class="action-icon">🏅</div>
              <h3>排行榜</h3>
              <p>查看全球玩家排行榜</p>
            </router-link>
          </div>
        </div>

        <!-- 最近活动 -->
        <div class="recent-activity">
          <h2>最近活动</h2>
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon">🎮</div>
              <div class="activity-content">
                <p>欢迎来到爆炸单词游戏！</p>
                <span class="activity-time">刚刚</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/utils/auth.js'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const { user, logout, getCurrentUser } = useAuth()

    const handleLogout = () => {
      logout()
      router.push('/login')
    }

    onMounted(async () => {
      // 获取最新的用户信息
      try {
        const result = await getCurrentUser()
        if (!result.success) {
          console.warn('获取用户信息失败，可能需要重新登录')
          // 如果获取用户信息失败，认证管理器会自动处理跳转
        }
      } catch (error) {
        console.error('Dashboard初始化失败:', error)
      }
    })

    return {
      user: computed(() => user.value),
      handleLogout
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f8fafc;
}

.dashboard-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.welcome-text {
  font-size: 16px;
  color: #4a5568;
}

.logout-button {
  padding: 8px 16px;
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: #c53030;
}

.dashboard-main {
  padding: 20px;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f7fafc;
  border-radius: 12px;
}

.stat-info h3 {
  font-size: 14px;
  color: #718096;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.quick-actions, .recent-activity {
  margin-bottom: 40px;
}

.quick-actions h2, .recent-activity h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 20px 0;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
  display: block;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.action-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.action-card p {
  font-size: 14px;
  color: #718096;
  margin: 0;
  line-height: 1.5;
}

.activity-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 20px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f7fafc;
  border-radius: 8px;
}

.activity-content {
  flex: 1;
}

.activity-content p {
  font-size: 14px;
  color: #1a202c;
  margin: 0 0 4px 0;
}

.activity-time {
  font-size: 12px;
  color: #718096;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .dashboard-main {
    padding: 10px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>