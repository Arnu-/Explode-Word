<template>
  <div class="game-panel">
    <!-- 模式选择遮罩层 -->
    <div v-if="showModeSelection" class="mode-selection-overlay">
      <div class="mode-selection-container">
        <h2 class="mode-title">选择游戏模式</h2>
        <div class="mode-options">
          <div class="mode-card training-mode" @click="selectMode('training')">
            <div class="mode-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L3 7L12 12L21 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 17L12 22L21 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 12L12 17L21 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="mode-name">训练模式</h3>
            <p class="mode-description">可以看见英文和中文<br>适合学习和练习</p>
          </div>
          
          <div class="mode-card challenge-mode" @click="selectMode('challenge')">
            <div class="mode-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="mode-name">挑战模式</h3>
            <p class="mode-description">只能看见中文<br>考验你的记忆力</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 顶部导航栏 -->
    <header class="game-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M15 18L9 12L15 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="level-info">
          <span class="level-text">选择关卡 第一关：小试牛刀</span>
        </div>
      </div>
      <div class="header-right">
        <div class="user-avatar">
          <span class="avatar-text">大</span>
          <span class="username">师傅</span>
        </div>
        <div class="coins">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" fill="#FFD700"/>
            <text x="12" y="16" text-anchor="middle" fill="#000" font-size="12" font-weight="bold">¥</text>
          </svg>
          <span>3,250</span>
        </div>
        <button class="settings-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="3" stroke="white" stroke-width="2"/>
            <path d="M12 1v6m0 10v6m11-7h-6m-10 0H1m15.5-3.5L19 4m-14 14l2.5-2.5M4 4l2.5 2.5m11 11L19 19" stroke="white" stroke-width="2"/>
          </svg>
        </button>
      </div>
    </header>

    <div class="game-content">
      <!-- 左侧统计面板 -->
      <aside class="stats-panel">
        <div class="stat-item">
          <span class="stat-label">得分：</span>
          <span class="stat-value">{{ score }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">用时：</span>
          <span class="stat-value">{{ formatTime(timeUsed) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">剩余：</span>
          <span class="stat-value">{{ remainingWords }}个单词</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">错误：</span>
          <span class="stat-value">{{ errors }}次</span>
        </div>
        
        <!-- 游戏控制按钮 -->
        <div class="game-controls">
          <button class="control-btn pause-btn" @click="pauseGame">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
              <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
            </svg>
            暂停
          </button>
          <button class="control-btn exit-btn" @click="exitGame">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="16,17 21,12 16,7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            退出
          </button>
        </div>
      </aside>

      <!-- 中央游戏区域 -->
      <main class="game-area">
        <div class="word-cards-container">
          <div 
            v-for="(word, index) in wordCards" 
            :key="index"
            class="word-card"
            :class="[`difficulty-${word.difficulty}`, { 'completed': word.completed }]"
            :style="{ 
              left: word.position.x + 'px', 
              top: word.position.y + 'px' 
            }"
          >
            <div class="difficulty-label">{{ getDifficultyLabel(word.difficulty) }}</div>
            <div v-if="gameMode === 'training'" class="english-word">{{ word.english }}</div>
            <div class="chinese-word">{{ word.chinese }}</div>
          </div>
        </div>
      </main>
    </div>

    <!-- 底部输入区域 -->
    <footer class="input-section">
      <!-- 帮助按钮 -->
      <div class="help-section">
        <button class="help-btn" @click="useHelp">
          <span>帮助</span>
        </button>
        <div class="help-count">X{{ helpCount }}</div>
      </div>

      <!-- 输入框 -->
      <div class="input-container">
        <input 
          v-model="currentInput" 
          type="text" 
          class="word-input"
          :placeholder="inputPlaceholder"
          @keyup.enter="submitWord"
          ref="wordInput"
        />
      </div>

      <!-- 虚拟键盘 -->
      <div class="virtual-keyboard">
        <div class="keyboard-row">
          <button 
            v-for="key in keyboardRow1" 
            :key="key"
            class="key-btn"
            @click="inputKey(key)"
          >
            {{ key }}
          </button>
        </div>
        <div class="keyboard-row">
          <button 
            v-for="key in keyboardRow2" 
            :key="key"
            class="key-btn"
            @click="inputKey(key)"
          >
            {{ key }}
          </button>
        </div>
        <div class="keyboard-row">
          <button 
            v-for="key in keyboardRow3" 
            :key="key"
            class="key-btn"
            @click="inputKey(key)"
          >
            {{ key }}
          </button>
        </div>
      </div>
    </footer>

    <!-- 底部导航栏 -->
    <nav class="bottom-nav">
      <div class="nav-item" @click="$router.push('/')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>首页</span>
      </div>
      <div class="nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>排行榜</span>
      </div>
      <div class="nav-item" @click="$router.push({ name: 'levels' })">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M15 10L11 14L17 20L21 16L15 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>关卡</span>
      </div>
      <div class="nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M12.5 7C12.5 9.20914 10.7091 11 8.5 11C6.29086 11 4.5 9.20914 4.5 7C4.5 4.79086 6.29086 3 8.5 3C10.7091 3 12.5 4.79086 12.5 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>商店</span>
      </div>
      <div class="nav-item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>我的</span>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'GamePanel',
  props: {
    levelId: {
      type: [String, Number],
      default: 1
    }
  },
  data() {
    return {
      showModeSelection: true,
      gameMode: null, // 'training' 或 'challenge'
      score: 368,
      timeUsed: 90, // 秒
      remainingWords: 31,
      errors: 2,
      helpCount: 3,
      currentInput: '',
      inputPlaceholder: 'APP',
      
      // 虚拟键盘布局
      keyboardRow1: ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
      keyboardRow2: ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
      keyboardRow3: ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
      
      // 单词卡片数据
      wordCards: [
        {
          english: 'cat',
          chinese: '猫',
          difficulty: 1,
          completed: false,
          position: { x: 100, y: 50 }
        },
        {
          english: 'apple',
          chinese: '苹果',
          difficulty: 2,
          completed: false,
          position: { x: 400, y: 20 }
        },
        {
          english: 'dog',
          chinese: '狗',
          difficulty: 1,
          completed: false,
          position: { x: 650, y: 50 }
        },
        {
          english: 'pineapple',
          chinese: '菠萝',
          difficulty: 3,
          completed: false,
          position: { x: 300, y: 120 }
        },
        {
          english: 'book',
          chinese: '书',
          difficulty: 1,
          completed: false,
          position: { x: 550, y: 130 }
        },
        {
          english: 'water',
          chinese: '水',
          difficulty: 1,
          completed: false,
          position: { x: 150, y: 200 }
        },
        {
          english: 'house',
          chinese: '房子',
          difficulty: 1,
          completed: false,
          position: { x: 450, y: 180 }
        },
        {
          english: 'computer',
          chinese: '电脑',
          difficulty: 2,
          completed: false,
          position: { x: 700, y: 200 }
        },
        {
          english: 'beautiful',
          chinese: '美丽的',
          difficulty: 3,
          completed: false,
          position: { x: 350, y: 250 }
        },
        {
          english: 'congratulation',
          chinese: '祝贺',
          difficulty: 4,
          completed: false,
          position: { x: 500, y: 280 }
        }
      ]
    }
  },
  methods: {
    selectMode(mode) {
      this.gameMode = mode
      this.showModeSelection = false
      console.log('选择模式:', mode)
    },
    
    goBack() {
      this.$router.push({ name: 'levels' })
    },
    
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
    },
    
    getDifficultyLabel(difficulty) {
      const labels = {
        1: '一级难度',
        2: '二级难度', 
        3: '三级难度',
        4: '四级难度'
      }
      return labels[difficulty] || '一级难度'
    },
    
    inputKey(key) {
      this.currentInput += key
    },
    
    submitWord() {
      // 提交单词逻辑
      console.log('提交单词:', this.currentInput)
      this.currentInput = ''
    },
    
    useHelp() {
      if (this.helpCount > 0) {
        this.helpCount--
        // 帮助逻辑
        console.log('使用帮助')
      }
    },
    
    pauseGame() {
      // 暂停游戏逻辑
      console.log('暂停游戏')
      // 可以在这里添加暂停弹窗或状态切换
    },
    
    exitGame() {
      // 退出游戏逻辑
      console.log('退出游戏')
      this.$router.push({ name: 'levels' })
    }
  }
}
</script>

<style scoped>
.game-panel {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
}

/* 模式选择遮罩层 */
.mode-selection-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.mode-selection-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.mode-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 30px;
  color: white;
}

.mode-options {
  display: flex;
  gap: 30px;
  justify-content: center;
}

.mode-card {
  width: 200px;
  height: 250px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 30px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.mode-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.training-mode:hover {
  border-color: #74b9ff;
  box-shadow: 0 10px 30px rgba(116, 185, 255, 0.3);
}

.challenge-mode:hover {
  border-color: #fd79a8;
  box-shadow: 0 10px 30px rgba(253, 121, 168, 0.3);
}

.mode-icon {
  margin-bottom: 20px;
  color: white;
}

.mode-name {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: white;
}

.mode-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}

/* 顶部导航栏 */
.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.level-text {
  font-size: 16px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-text {
  width: 32px;
  height: 32px;
  background: #FFD700;
  color: #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.username {
  font-size: 14px;
}

.coins {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.settings-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.settings-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 游戏内容区域 */
.game-content {
  flex: 1;
  display: flex;
  padding: 20px;
  gap: 20px;
}

/* 左侧统计面板 */
.stats-panel {
  width: 200px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  padding: 24px;
  height: fit-content;
  backdrop-filter: blur(10px);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 16px;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
}

.stat-value {
  font-weight: bold;
  color: white;
}

/* 游戏控制按钮 */
.game-controls {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.pause-btn {
  background: rgba(255, 193, 7, 0.8);
}

.pause-btn:hover {
  background: rgba(255, 193, 7, 1);
  transform: translateY(-1px);
}

.exit-btn {
  background: rgba(220, 53, 69, 0.8);
}

.exit-btn:hover {
  background: rgba(220, 53, 69, 1);
  transform: translateY(-1px);
}

/* 游戏区域 */
.game-area {
  flex: 1;
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #00BFFF;
  border-radius: 16px;
  min-height: 400px;
  backdrop-filter: blur(10px);
}

.word-cards-container {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 20px;
}

.word-card {
  position: absolute;
  width: 120px;
  height: 80px;
  border-radius: 12px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-size: 14px;
  text-align: center;
}

.word-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.difficulty-1 {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
}

.difficulty-2 {
  background: linear-gradient(135deg, #55efc4, #00b894);
}

.difficulty-3 {
  background: linear-gradient(135deg, #fdcb6e, #e17055);
}

.difficulty-4 {
  background: linear-gradient(135deg, #fd79a8, #e84393);
}

.difficulty-label {
  font-size: 10px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.english-word {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 2px;
}

.chinese-word {
  font-size: 12px;
  opacity: 0.9;
}

.word-card.completed {
  opacity: 0.5;
  transform: scale(0.9);
}

/* 底部输入区域 */
.input-section {
  background: rgba(0, 0, 0, 0.4);
  padding: 20px;
  backdrop-filter: blur(10px);
}

.help-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.help-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.help-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.help-count {
  font-size: 18px;
  font-weight: bold;
}

.input-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.word-input {
  width: 300px;
  height: 50px;
  background: white;
  border: none;
  border-radius: 8px;
  padding: 0 16px;
  font-size: 18px;
  text-align: center;
  outline: none;
}

/* 虚拟键盘 */
.virtual-keyboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.keyboard-row {
  display: flex;
  gap: 6px;
}

.key-btn {
  width: 45px;
  height: 45px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  color: #333;
}

.key-btn:hover {
  background: white;
  transform: translateY(-1px);
}

.key-btn:active {
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.7);
}

/* 底部导航栏 */
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 12px 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mode-options {
    flex-direction: column;
    gap: 20px;
  }
  
  .mode-card {
    width: 250px;
    height: 200px;
  }
  
  .game-content {
    flex-direction: column;
    padding: 10px;
  }
  
  .stats-panel {
    width: 100%;
    display: flex;
    justify-content: space-around;
    padding: 16px;
  }
  
  .stat-item {
    margin-bottom: 0;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  
  .word-card {
    width: 100px;
    height: 70px;
    font-size: 12px;
  }
  
  .virtual-keyboard {
    transform: scale(0.9);
  }
}
</style>