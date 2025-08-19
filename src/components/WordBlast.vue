<template>
  <div class="game-container">
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

    <!-- 游戏标题区 -->
    <div class="game-title">
      <h1 class="main-title">单词爆破</h1>
      <p class="subtitle">炸裂词汇，挑战极限</p>
    </div>

    <!-- 主按钮区域 -->
    <div class="button-container">
      <button class="game-button start-button" @click="navigateToLevels">
        开始游戏
      </button>
      <button class="game-button leaderboard-button">
        排行榜
      </button>
      <button class="game-button settings-button">
        游戏设置
      </button>
    </div>

    <!-- 装饰元素区 -->
    <div class="decoration left-decoration">
      <div class="letter-container">
        <div class="letter letter-a">A</div>
        <div class="letter letter-z">Z</div>
        <div class="letter letter-b">B</div>
      </div>
    </div>
    
    <div class="decoration right-decoration">
      <div class="letter-container">
        <div class="letter letter-q">Q</div>
        <div class="letter letter-w">W</div>
        <div class="letter letter-e">E</div>
      </div>
    </div>

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

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function navigateToLevels() {
  router.push('/levels');
}
</script>

<style scoped>
* {
  font-family: 'Noto Sans SC', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.game-container {
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

/* 游戏标题 */
.game-title {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 10;
}

.main-title {
  font-size: 4rem;
  font-weight: bold;
  background: linear-gradient(to right, #f9a8d4, #c4b5fd, #a5b4fc);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.5));
}

@media (min-width: 768px) {
  .main-title {
    font-size: 5rem;
  }
}

@media (min-width: 1024px) {
  .main-title {
    font-size: 6rem;
  }
}

.subtitle {
  margin-top: 1rem;
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
}

/* 按钮区域 */
.button-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  z-index: 10;
  width: 100%;
  max-width: 20rem;
}

.game-button {
  width: 100%;
  padding: 1rem 0;
  border-radius: 0.75rem;
  color: white;
  font-weight: bold;
  font-size: 1.25rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.game-button:hover {
  transform: scale(1.05);
}

.start-button {
  background: linear-gradient(to right, #ec4899, #9333ea);
  box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.3);
}

.start-button:hover {
  box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.5);
}

.leaderboard-button {
  background: linear-gradient(to right, #3b82f6, #4f46e5);
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
}

.leaderboard-button:hover {
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5);
}

.settings-button {
  background: linear-gradient(to right, #8b5cf6, #d946ef);
  box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.3);
}

.settings-button:hover {
  box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.5);
}

/* 装饰元素 */
.decoration {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.6;
}

@media (max-width: 1023px) {
  .decoration {
    display: none;
  }
}

.left-decoration {
  left: 16.666%;
}

.right-decoration {
  right: 16.666%;
}

.letter-container {
  position: relative;
}

.letter {
  position: absolute;
  font-weight: bold;
  opacity: 0.7;
}

.letter-a {
  top: -4rem;
  left: -2rem;
  font-size: 3rem;
  color: #f9a8d4;
  transform: rotate(12deg);
}

.letter-z {
  top: 2rem;
  left: -1rem;
  font-size: 2.5rem;
  color: #93c5fd;
  transform: rotate(-15deg);
}

.letter-b {
  top: 5rem;
  left: 3rem;
  font-size: 3.5rem;
  color: #c4b5fd;
  transform: rotate(6deg);
}

.letter-q {
  top: -3rem;
  right: -1rem;
  font-size: 3rem;
  color: #fde047;
  transform: rotate(-12deg);
}

.letter-w {
  top: 2.5rem;
  right: -2rem;
  font-size: 2.5rem;
  color: #86efac;
  transform: rotate(15deg);
}

.letter-e {
  top: 6rem;
  right: 2rem;
  font-size: 3.5rem;
  color: #a5b4fc;
  transform: rotate(-6deg);
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
