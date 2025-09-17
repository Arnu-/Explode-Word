<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from './utils/auth.js'

const router = useRouter()
const route = useRoute()

// 使用统一的认证状态管理
const { isAuthenticated, user: currentUser, logout } = useAuth()

// 控制退出游戏确认弹窗
const showExitConfirm = ref(false)

// 控制用户菜单显示
const showUserMenu = ref(false)

// 用户等级和金币数据
const userLevel = ref(42)
const userLevelText = ref('大师级')
const userCoins = ref(3250)

// 判断当前是否在游戏中
const isInGame = computed(() => {
  return route.name === 'GamePanel'
})

// 判断是否显示用户信息（等级和金币）
const shouldShowUserInfo = computed(() => {
  return isAuthenticated.value && currentUser.value
})

// 初始化认证状态（现在由 auth.js 自动处理）
const initAuth = async () => {
  // auth.js 会自动初始化认证状态
  loadUserData()
}

// 点击返回首页按钮
const handleGoHome = () => {
  if (isInGame.value) {
    // 如果在游戏中，显示确认弹窗
    showExitConfirm.value = true
  } else {
    // 直接回到游戏首页
    router.push({ name: 'wordblast' })
  }
}

// 确认退出游戏
const confirmExit = () => {
  showExitConfirm.value = false
  router.push({ name: 'wordblast' })
}

// 取消退出
const cancelExit = () => {
  showExitConfirm.value = false
}

// 点击设置按钮
const handleSettings = () => {
  // 跳转到设置页面或打开设置弹窗
  router.push({ name: 'settings' })
}

// 点击用户头像
const handleUserProfile = () => {
  try {
    if (isAuthenticated.value) {
      router.push({ name: 'profile' })
      showUserMenu.value = false
    } else {
      router.push({ name: 'login' })
    }
  } catch (error) {
    console.error('跳转用户资料页面失败:', error)
    router.push({ name: 'login' })
  }
}

// 切换用户菜单显示状态
const toggleUserMenu = () => {
  console.log('用户头像被点击，当前认证状态:', isAuthenticated.value)
  if (isAuthenticated.value) {
    showUserMenu.value = !showUserMenu.value
    console.log('菜单显示状态:', showUserMenu.value)
  } else {
    router.push({ name: 'login' })
  }
}

// 退出登录
const handleLogout = () => {
  console.log('退出登录被点击')
  try {
    // 使用统一的认证管理器退出登录
    logout()
    showUserMenu.value = false
    
    console.log('认证状态已重置，准备跳转到登录页')
    
    // 跳转到登录页
    router.push({ name: 'login' })
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}

// 点击外部关闭用户菜单
const closeUserMenu = () => {
  showUserMenu.value = false
}

// 加载用户数据
const loadUserData = async () => {
  try {
    if (isAuthenticated.value && currentUser.value) {
      // 这里可以从API获取用户的等级和金币数据
      // 暂时使用模拟数据
      userLevel.value = currentUser.value.level || 42
      userLevelText.value = getLevelText(userLevel.value)
      userCoins.value = currentUser.value.coins || 3250
    }
  } catch (error) {
    console.warn('加载用户数据失败:', error)
    // 使用默认值
    userLevel.value = 42
    userLevelText.value = '大师级'
    userCoins.value = 3250
  }
}

// 获取等级文本
const getLevelText = (level) => {
  if (level >= 50) return '传奇'
  if (level >= 40) return '大师级'
  if (level >= 30) return '专家级'
  if (level >= 20) return '高级'
  if (level >= 10) return '中级'
  return '初级'
}

// 监听认证状态变化
watch([isAuthenticated, currentUser], () => {
  loadUserData()
}, { immediate: false })

// 组件挂载时初始化
onMounted(() => {
  initAuth()
})
</script>

<template>
  <div class="app-container">
    <!-- 背景区域 - 烟花效果 -->
    <div class="background">
      <div class="firework firework-1"></div>
      <div class="firework firework-2"></div>
      <div class="firework firework-3"></div>
      <div class="firework firework-4"></div>
      <div class="firework firework-5"></div>
    </div>

    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="navbar-left">
        <button class="home-button" @click="handleGoHome">
          <i class="fa-solid fa-house"></i>
        </button>
      </div>
      <div class="navbar-brand">
        <div class="logo">
          <i class="fa-solid fa-bomb"></i>
        </div>
        <span class="brand-name">WordBlast</span>
      </div>
      <div class="navbar-actions">
        <!-- 用户等级信息 - 仅在登录时显示 -->
        <div v-if="shouldShowUserInfo" class="user-level">
          <div class="level-badge">
            <span>{{ userLevel }}</span>
          </div>
          <span class="level-text">{{ userLevelText }}</span>
        </div>
        
        <!-- 游戏币信息 - 仅在登录时显示 -->
        <div v-if="shouldShowUserInfo" class="coins">
          <i class="fa-solid fa-coins coin-icon"></i>
          <span class="coin-amount">{{ userCoins.toLocaleString() }}</span>
        </div>
        
        <!-- 设置按钮 -->
        <button class="settings-button" @click="handleSettings">
          <i class="fa-solid fa-gear"></i>
        </button>
        
        <!-- 用户头像和菜单 -->
        <div class="user-menu-container" v-if="isAuthenticated">
          <div class="user-avatar" @click="toggleUserMenu">
            <i class="fa-solid fa-user"></i>
          </div>
          
    <!-- 点击外部关闭用户菜单 -->
    <div v-if="showUserMenu" class="menu-overlay" @click="closeUserMenu"></div>

          <!-- 用户下拉菜单 -->
          <div v-if="showUserMenu" class="user-dropdown" @click.stop>
            <div class="dropdown-item" @click="handleUserProfile">
              <i class="fa-solid fa-user"></i>
              <span>个人资料</span>
            </div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item logout-item" @click="handleLogout">
              <i class="fa-solid fa-sign-out-alt"></i>
              <span>退出登录</span>
            </div>
          </div>
        </div>
        
        <!-- 未登录时的用户头像 -->
        <div v-else class="user-avatar" @click="handleUserProfile">
          <i class="fa-solid fa-user"></i>
        </div>
      </div>
    </nav>

    <!-- 退出游戏确认弹窗 -->
    <div v-if="showExitConfirm" class="modal-overlay" @click="cancelExit">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>退出游戏</h3>
        </div>
        <div class="modal-body">
          <p>您确定要退出当前游戏吗？</p>
          <p class="warning-text">游戏进度将不会保存</p>
        </div>
        <div class="modal-actions">
          <button class="cancel-btn" @click="cancelExit">取消</button>
          <button class="confirm-btn" @click="confirmExit">确定退出</button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 底部信息栏 -->
    <div class="footer">
      <div class="copyright">© 2023 单词爆破 | 版本 1.0.2</div>
      <div class="social-links">
        <a href="#" class="social-link">
          <i class="fa-brands fa-twitter"></i>
        </a>
        <a href="#" class="social-link">
          <i class="fa-brands fa-discord"></i>
        </a>
        <a href="#" class="social-link">
          <i class="fa-brands fa-instagram"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<style>
* {
  font-family: 'Noto Sans SC', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
  display: block;
}

.app-container {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(to bottom, #4a1d96, #312e81, #000000);
  overflow: hidden;
}

/* 背景烟花效果 */
.background {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.firework {
  position: absolute;
  border-radius: 50%;
  filter: blur(15px);
  animation: pulse 3s infinite;
}

.firework-1 {
  top: 25%;
  left: 25%;
  width: 6rem;
  height: 6rem;
  background-color: #ec4899;
  opacity: 0.3;
}

.firework-2 {
  top: 33%;
  right: 33%;
  width: 8rem;
  height: 8rem;
  background-color: #3b82f6;
  opacity: 0.2;
  animation-delay: 1s;
}

.firework-3 {
  bottom: 25%;
  left: 33%;
  width: 10rem;
  height: 10rem;
  background-color: #eab308;
  opacity: 0.25;
  animation-delay: 2s;
}

.firework-4 {
  top: 50%;
  right: 25%;
  width: 9rem;
  height: 9rem;
  background-color: #22c55e;
  opacity: 0.2;
  animation-delay: 1.5s;
}

.firework-5 {
  bottom: 33%;
  right: 25%;
  width: 7rem;
  height: 7rem;
  background-color: #a855f7;
  opacity: 0.3;
  animation-delay: 0.5s;
}

/* 导航栏 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4rem;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  z-index: 10;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.home-button {
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.home-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #f9a8d4;
}

.home-button i {
  font-size: 1.25rem;
}

.navbar-brand {
  display: flex;
  align-items: center;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.logo {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(to right, #ec4899, #a855f7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo i {
  color: white;
  font-size: 1.25rem;
}

.brand-name {
  margin-left: 0.75rem;
  color: white;
  font-weight: 500;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* 用户等级样式 */
.user-level {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.level-badge {
  width: 2rem;
  height: 2rem;
  background: linear-gradient(90deg, #FACC15 0%, #F97316 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
}

.level-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
}

/* 游戏币样式 */
.coins {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 0.75rem;
  border-radius: 1rem;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.coin-icon {
  font-size: 1rem;
  color: #fbbf24;
}

.coin-amount {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
}

.settings-button {
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.settings-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #f9a8d4;
}

.settings-button i {
  font-size: 1.25rem;
}

.user-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(to right, #60a5fa, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
}

.user-avatar:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
}

/* 用户菜单容器 */
.user-menu-container {
  position: relative;
  z-index: 1002;
}

/* 用户下拉菜单 */
.user-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: rgba(30, 27, 75, 0.95);
  backdrop-filter: blur(8px);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  min-width: 160px;
  z-index: 9999;
  overflow: hidden;
  pointer-events: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.875rem;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.dropdown-item i {
  font-size: 1rem;
  width: 1rem;
  text-align: center;
}

.dropdown-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 0.25rem 0;
}

.logout-item {
  color: #fca5a5;
}

.logout-item:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

/* 菜单遮罩层 */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 1000px;
  z-index: 998;
}

/* 主内容区域 */
.main-content {
  padding-top: 4rem; /* 与导航栏高度相同 */
  padding-bottom: 3rem; /* 与底部栏高度相同 */
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* 底部信息栏 */
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3rem;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  z-index: 10;
}

.social-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.social-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s;
}

.social-link:hover {
  color: #f9a8d4;
}

.social-link i {
  font-size: 1.125rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, #1e1b4b, #312e81);
  border-radius: 1rem;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
}

.modal-body {
  margin-bottom: 2rem;
  text-align: center;
}

.modal-body p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.warning-text {
  color: #fbbf24 !important;
  font-size: 0.875rem !important;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.cancel-btn, .confirm-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

.cancel-btn {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cancel-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.confirm-btn {
  background: linear-gradient(to right, #ef4444, #dc2626);
  color: white;
}

.confirm-btn:hover {
  background: linear-gradient(to right, #dc2626, #b91c1c);
  transform: translateY(-1px);
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.05);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar {
    padding: 0 1rem;
  }
  
  .navbar-actions {
    gap: 0.75rem;
  }
  
  .user-level .level-text {
    display: none; /* 在小屏幕上隐藏等级文字 */
  }
  
  .coins {
    padding: 0.375rem 0.5rem;
  }
  
  .coin-amount {
    font-size: 0.75rem;
  }
  
  .brand-name {
    display: none; /* 在小屏幕上隐藏品牌名称 */
  }
}

@media (max-width: 480px) {
  .navbar-actions {
    gap: 0.5rem;
  }
  
  .level-badge {
    width: 1.75rem;
    height: 1.75rem;
    font-size: 0.625rem;
  }
  
  .coins {
    padding: 0.25rem 0.5rem;
  }
  
  .coin-amount {
    font-size: 0.625rem;
  }
  
  .user-avatar {
    width: 2rem;
    height: 2rem;
  }
  
  .settings-button {
    padding: 0.375rem;
  }
  
  .settings-button i {
    font-size: 1rem;
  }
}
</style>