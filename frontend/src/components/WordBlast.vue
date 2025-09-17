<template>
  <div class="home-content">
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
      <button class="game-button settings-button" @click="navigateToConfig">
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
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function navigateToLevels() {
  router.push('/sections');
}

function navigateToConfig() {
  router.push('/config');
}
</script>

<style scoped>
.home-content {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 游戏标题 */
.game-title {
  position: relative;
  text-align: center;
  z-index: 10;
  margin-bottom: 5rem;
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
</style>
