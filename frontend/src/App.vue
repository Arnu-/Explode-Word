<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 控制退出游戏确认弹窗
const showExitConfirm = ref(false)

// 判断当前是否在游戏中
const isInGame = computed(() => {
  return route.name === 'GamePanel'
})

// 点击返回首页按钮
const handleGoHome = () => {
  if (isInGame.value) {
    // 如果在游戏中，显示确认弹窗
    showExitConfirm.value = true
  } else {
    // 直接回到首页
    router.push('/')
  }
}

// 确认退出游戏
const confirmExit = () => {
  showExitConfirm.value = false
  router.push('/')
}

// 取消退出
const cancelExit = () => {
  showExitConfirm.value = false
}
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
        <button class="settings-button">
          <i class="fa-solid fa-gear"></i>
        </button>
        <div class="user-avatar">
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
  gap: 1rem;
}

.settings-button {
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s;
}

.settings-button:hover {
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
</style>
