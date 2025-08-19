<script setup>
// 导入需要的组件和功能
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

.navbar-brand {
  display: flex;
  align-items: center;
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
