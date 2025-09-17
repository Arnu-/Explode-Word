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
            :key="word.id"
            class="word-card"
            :class="[
              { 
                'completed': word.completed,
                'exploding': word.exploding,
                'dragging': word.isDragging
              }
            ]"
            :style="{ 
              left: word.position.x + 'px', 
              top: word.position.y + 'px',
              backgroundColor: gameConfig.levelColors[`level${word.difficulty}`] || '#f8f9fa'
            }"
            @mousedown="startDrag($event, index)"
            @touchstart="startDrag($event, index)"
          >
            <div class="difficulty-label">{{ getDifficultyLabel(word.difficulty) }}</div>
            <div 
              v-if="gameMode === 'training'" 
              class="english-word"
              :style="{ fontSize: gameConfig.englishFontSize + 'px' }"
            >
              {{ word.english }}
            </div>
            <div 
              class="chinese-word"
              :style="{ fontSize: gameConfig.chineseFontSize + 'px' }"
            >
              {{ word.chinese }}
            </div>
            
            <!-- 爆炸碎片覆盖层 -->
            <div v-if="word.exploding" class="explosion-fragments">
              <div 
                v-for="fragmentIndex in 9" 
                :key="fragmentIndex"
                class="fragment"
                :class="`fragment-${fragmentIndex}`"
                :style="{ background: getFragmentColor(word.difficulty) }"
              ></div>
              
              <!-- 加分提示 -->
              <div class="score-popup">
                +{{ getScoreByDifficulty(word.difficulty) }}
              </div>
            </div>
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
          @keydown="handleInputKeyDown"
          @input="handleInputChange"
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
            :class="{ 'key-pressed': isKeyPressed(key) }"
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
            :class="{ 'key-pressed': isKeyPressed(key) }"
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
            :class="{ 'key-pressed': isKeyPressed(key) }"
            @click="inputKey(key)"
          >
            {{ key }}
          </button>
        </div>
      </div>
    </footer>

    <!-- 底部导航栏 -->
    <nav class="bottom-nav">
      <div class="nav-item" @click="$router.push('/game')">
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
      <div class="nav-item" @click="$router.push('/profile')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>我的</span>
      </div>
    </nav>
  </div>
</template>

<script>
import { getGameConfig, onConfigUpdate, offConfigUpdate } from '@/utils/gameConfig.js'

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
      inputPlaceholder: '',
      gameConfig: getGameConfig(),
      
      // 虚拟键盘布局
      keyboardRow1: ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
      keyboardRow2: ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
      keyboardRow3: ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
      
      // 按键状态
      pressedKeys: new Set(),
      
      // 覆盖检测定时器
      overlapCheckTimer: null,
      
      // 拖拽相关状态
      isDragging: false,
      dragStartPos: { x: 0, y: 0 },
      dragCardIndex: -1,
      dragOffset: { x: 0, y: 0 },
      
      // 单词卡片数据
      wordCards: [
        {
          id: 1,
          english: 'cat',
          chinese: '猫',
          difficulty: 1,
          completed: false,
          position: { x: 100, y: 50 },
          isDragging: false
        },
        {
          id: 2,
          english: 'apple',
          chinese: '苹果',
          difficulty: 2,
          completed: false,
          position: { x: 400, y: 20 },
          isDragging: false
        },
        {
          id: 3,
          english: 'dog',
          chinese: '狗',
          difficulty: 1,
          completed: false,
          position: { x: 650, y: 50 },
          isDragging: false
        },
        {
          id: 4,
          english: 'pineapple',
          chinese: '菠萝',
          difficulty: 3,
          completed: false,
          position: { x: 300, y: 120 },
          isDragging: false
        },
        {
          id: 5,
          english: 'book',
          chinese: '书',
          difficulty: 1,
          completed: false,
          position: { x: 550, y: 130 },
          isDragging: false
        },
        {
          id: 6,
          english: 'water',
          chinese: '水',
          difficulty: 1,
          completed: false,
          position: { x: 150, y: 200 },
          isDragging: false
        },
        {
          id: 7,
          english: 'house',
          chinese: '房子',
          difficulty: 1,
          completed: false,
          position: { x: 450, y: 180 },
          isDragging: false
        },
        {
          id: 8,
          english: 'computer',
          chinese: '电脑',
          difficulty: 2,
          completed: false,
          position: { x: 700, y: 200 },
          isDragging: false
        },
        {
          id: 9,
          english: 'beautiful',
          chinese: '美丽的',
          difficulty: 3,
          completed: false,
          position: { x: 350, y: 250 },
          isDragging: false
        },
        {
          id: 10,
          english: 'congratulation',
          chinese: '祝贺',
          difficulty: 4,
          completed: false,
          position: { x: 500, y: 280 },
          isDragging: false
        }
      ]
    }
  },
  mounted() {
    // 添加键盘事件监听
    document.addEventListener('keydown', this.handleKeyDown)
    document.addEventListener('keyup', this.handleKeyUp)
    
    // 添加拖拽事件监听
    document.addEventListener('mousemove', this.handleDrag)
    document.addEventListener('mouseup', this.endDrag)
    document.addEventListener('touchmove', this.handleDrag, { passive: false })
    document.addEventListener('touchend', this.endDrag)
    
    // 监听配置更新
    this.configUpdateHandler = (config) => {
      this.gameConfig = config
    }
    onConfigUpdate(this.configUpdateHandler)
    
    // 聚焦输入框
    this.$nextTick(() => {
      if (this.$refs.wordInput) {
        this.$refs.wordInput.focus()
      }
    })
  },
  beforeUnmount() {
    // 移除键盘事件监听
    document.removeEventListener('keydown', this.handleKeyDown)
    document.removeEventListener('keyup', this.handleKeyUp)
    
    // 移除拖拽事件监听
    document.removeEventListener('mousemove', this.handleDrag)
    document.removeEventListener('mouseup', this.endDrag)
    document.removeEventListener('touchmove', this.handleDrag)
    document.removeEventListener('touchend', this.endDrag)
    
    // 移除配置更新监听
    if (this.configUpdateHandler) {
      offConfigUpdate(this.configUpdateHandler)
    }
  },
  methods: {
    // 处理键盘按下事件
    handleKeyDown(event) {
      const key = event.key.toUpperCase()
      
      // 只处理字母键
      if (key.match(/^[A-Z]$/)) {
        this.pressedKeys.add(key)
        
        // 如果游戏已开始且不在模式选择界面，且焦点不在输入框上
        if (!this.showModeSelection && event.target !== this.$refs.wordInput) {
          // 阻止默认行为
          event.preventDefault()
          // 将字母添加到输入框
          this.currentInput += key
          
          // 聚焦输入框
          if (this.$refs.wordInput) {
            this.$refs.wordInput.focus()
          }
        }
      }
      
      // 处理回车键
      if (event.key === 'Enter' && !this.showModeSelection) {
        this.submitWord()
      }
    },
    
    // 处理键盘释放事件
    handleKeyUp(event) {
      const key = event.key.toUpperCase()
      
      if (key.match(/^[A-Z]$/)) {
        // 延迟移除按键状态，创建按键效果
        setTimeout(() => {
          this.pressedKeys.delete(key)
        }, 150)
      }
    },
    
    // 检查按键是否被按下
    isKeyPressed(key) {
      return this.pressedKeys.has(key)
    },
    
    // 处理输入框键盘事件
    handleInputKeyDown(event) {
      const key = event.key.toUpperCase()
      
      // 处理字母键
      if (key.match(/^[A-Z]$/)) {
        this.pressedKeys.add(key)
        // 阻止默认输入，我们手动控制
        event.preventDefault()
        this.currentInput += key
      }
      
      // 处理退格键
      if (event.key === 'Backspace') {
        // 允许默认的退格行为
        return
      }
      
      // 阻止其他非字母字符的输入
      if (!key.match(/^[A-Z]$/) && event.key !== 'Backspace' && event.key !== 'Enter') {
        event.preventDefault()
      }
    },
    
    // 处理输入变化，确保只有大写字母
    handleInputChange(event) {
      this.currentInput = event.target.value.toUpperCase().replace(/[^A-Z]/g, '')
    },
    
    // 获取碎片颜色（根据难度）
    getFragmentColor(difficulty) {
      const colors = {
        1: 'linear-gradient(135deg, #74b9ff, #0984e3)',
        2: 'linear-gradient(135deg, #55efc4, #00b894)',
        3: 'linear-gradient(135deg, #fdcb6e, #e17055)',
        4: 'linear-gradient(135deg, #fd79a8, #e84393)'
      }
      return colors[difficulty] || colors[1]
    },
    selectMode(mode) {
      this.gameMode = mode
      this.showModeSelection = false
      
      // 选择模式后生成词卡位置
      this.generateRandomPositions()
      
      console.log('选择模式:', mode)
    },
    
    
    // 生成随机位置，逐项检测覆盖确保词卡不重叠
    generateRandomPositions() {
      // 延迟执行以确保DOM已渲染
      this.$nextTick(() => {
        const gameAreaElement = document.querySelector('.game-area')
        if (!gameAreaElement) {
          // 如果找不到游戏区域，使用默认值
          this.fallbackPositionGeneration()
          return
        }
        
        const rect = gameAreaElement.getBoundingClientRect()
        const gameArea = {
          width: Math.max(600, rect.width - 40),  // 减去padding，最小600px
          height: Math.max(300, rect.height - 40), // 减去padding，最小300px
          padding: 20
        }
        
        const cardSize = {
          width: 120,
          height: 80
        }
        
        // 已放置的位置数组，用于逐项检测
        const placedPositions = []
        
        // 逐个为每张词卡生成位置
        for (let i = 0; i < this.wordCards.length; i++) {
          let position = null
          let attempts = 0
          const maxAttempts = 50
          
          // 尝试为当前词卡找到不重叠的位置
          while (attempts < maxAttempts) {
            const candidatePosition = {
              x: Math.random() * (gameArea.width - cardSize.width) + gameArea.padding,
              y: Math.random() * (gameArea.height - cardSize.height) + gameArea.padding
            }
            
            // 检查是否与已放置的词卡重叠
            if (!this.isPositionOverlapping(candidatePosition, placedPositions, cardSize)) {
              position = candidatePosition
              break
            }
            
            attempts++
          }
          
          // 如果随机生成失败，使用网格布局
          if (!position) {
            position = this.generateGridPosition(i, gameArea, cardSize, placedPositions)
          }
          
          // 将位置添加到已放置数组中
          placedPositions.push(position)
          // 更新词卡位置
          this.wordCards[i].position = position
        }
      })
    },
    
    // 生成网格位置（当随机生成失败时的后备方案）
    generateGridPosition(index, gameArea, cardSize, placedPositions) {
      const cols = Math.min(5, Math.ceil(Math.sqrt(this.wordCards.length)))
      const rows = Math.ceil(this.wordCards.length / cols)
      const col = index % cols
      const row = Math.floor(index / cols)
      
      const cellWidth = gameArea.width / cols
      const cellHeight = gameArea.height / rows
      
      // 在网格单元内尝试多个位置
      for (let attempt = 0; attempt < 10; attempt++) {
        const offsetX = Math.random() * Math.max(0, cellWidth - cardSize.width)
        const offsetY = Math.random() * Math.max(0, cellHeight - cardSize.height)
        
        const position = {
          x: (col * cellWidth) + offsetX + gameArea.padding,
          y: (row * cellHeight) + offsetY + gameArea.padding
        }
        
        // 检查网格位置是否与已放置的词卡重叠
        if (!this.isPositionOverlapping(position, placedPositions, cardSize)) {
          return position
        }
      }
      
      // 如果网格位置也重叠，使用基础网格位置
      return {
        x: (col * cellWidth) + gameArea.padding,
        y: (row * cellHeight) + gameArea.padding
      }
    },
    
    // 后备位置生成方案
    fallbackPositionGeneration() {
      const gameArea = { width: 760, height: 350, padding: 20 }
      const cardSize = { width: 120, height: 80 }
      const positions = []
      
      this.wordCards.forEach((card, index) => {
        const cols = 5
        const rows = Math.ceil(this.wordCards.length / cols)
        const col = index % cols
        const row = Math.floor(index / cols)
        
        const cellWidth = gameArea.width / cols
        const cellHeight = gameArea.height / rows
        
        const offsetX = Math.random() * Math.max(0, cellWidth - cardSize.width)
        const offsetY = Math.random() * Math.max(0, cellHeight - cardSize.height)
        
        const position = {
          x: (col * cellWidth) + offsetX + gameArea.padding,
          y: (row * cellHeight) + offsetY + gameArea.padding
        }
        
        positions.push(position)
        this.wordCards[index].position = position
      })
    },
    
    // 检查位置是否重叠 - 使用更精确的中心距离算法
    isPositionOverlapping(newPosition, existingPositions, cardSize) {
      const minDistance = 8 // 减小最小间距，允许更紧密的布局
      
      return existingPositions.some(existingPos => {
        // 计算两个矩形中心点的距离
        const newCenterX = newPosition.x + cardSize.width / 2
        const newCenterY = newPosition.y + cardSize.height / 2
        const existingCenterX = existingPos.x + cardSize.width / 2
        const existingCenterY = existingPos.y + cardSize.height / 2
        
        const distanceX = Math.abs(newCenterX - existingCenterX)
        const distanceY = Math.abs(newCenterY - existingCenterY)
        
        // 使用中心距离判断，更精确
        const minCenterDistanceX = (cardSize.width / 2) + minDistance
        const minCenterDistanceY = (cardSize.height / 2) + minDistance
        
        return distanceX < minCenterDistanceX && distanceY < minCenterDistanceY
      })
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
      
      // 模拟按键效果
      this.pressedKeys.add(key)
      setTimeout(() => {
        this.pressedKeys.delete(key)
      }, 150)
      
      // 聚焦输入框
      if (this.$refs.wordInput) {
        this.$refs.wordInput.focus()
      }
    },
    
    submitWord() {
      if (!this.currentInput.trim()) return
      
      const inputWord = this.currentInput.trim().toLowerCase()
      console.log('提交单词:', inputWord)
      
      // 查找匹配的单词卡片
      const matchedCardIndex = this.wordCards.findIndex(card => 
        !card.completed && card.english.toLowerCase() === inputWord
      )
      
      if (matchedCardIndex !== -1) {
        // 找到匹配的单词
        const matchedCard = this.wordCards[matchedCardIndex]
        
        // 标记为完成状态，触发炸开动画
        this.wordCards[matchedCardIndex] = {
          ...matchedCard,
          completed: true,
          exploding: true
        }
        
        // 更新游戏统计
        this.score += this.getScoreByDifficulty(matchedCard.difficulty)
        this.remainingWords--
        
        // 延迟移除卡片（等待动画完成）
        setTimeout(() => {
          this.wordCards.splice(matchedCardIndex, 1)
        }, 800)
        
        console.log('单词正确！得分:', this.getScoreByDifficulty(matchedCard.difficulty))
      } else {
        // 单词错误
        this.errors++
        console.log('单词错误！')
        
        // 可以添加错误提示动画
        this.showErrorFeedback()
      }
      
      // 清空输入
      this.currentInput = ''
    },
    
    // 根据难度获取得分
    getScoreByDifficulty(difficulty) {
      const scores = {
        1: 10,
        2: 20,
        3: 30,
        4: 50
      }
      return scores[difficulty] || 10
    },
    
    // 显示错误反馈
    showErrorFeedback() {
      // 可以添加输入框红色闪烁效果
      const inputElement = this.$refs.wordInput
      if (inputElement) {
        inputElement.classList.add('error-shake')
        setTimeout(() => {
          inputElement.classList.remove('error-shake')
        }, 600)
      }
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
    },
    
    // 开始拖拽
    startDrag(event, cardIndex) {
      // 阻止默认行为和事件冒泡
      event.preventDefault()
      event.stopPropagation()
      
      // 如果词卡已完成或正在爆炸，不允许拖拽
      if (this.wordCards[cardIndex].completed || this.wordCards[cardIndex].exploding) {
        return
      }
      
      this.isDragging = true
      this.dragCardIndex = cardIndex
      
      // 获取鼠标/触摸位置
      const clientX = event.touches ? event.touches[0].clientX : event.clientX
      const clientY = event.touches ? event.touches[0].clientY : event.clientY
      
      // 记录拖拽开始位置
      this.dragStartPos = { x: clientX, y: clientY }
      
      // 计算鼠标相对于词卡的偏移
      const cardRect = event.currentTarget.getBoundingClientRect()
      this.dragOffset = {
        x: clientX - cardRect.left,
        y: clientY - cardRect.top
      }
      
      // 标记词卡为拖拽状态
      this.wordCards[cardIndex].isDragging = true
    },
    
    // 处理拖拽移动
    handleDrag(event) {
      if (!this.isDragging || this.dragCardIndex === -1) return
      
      event.preventDefault()
      
      // 获取当前鼠标/触摸位置
      const clientX = event.touches ? event.touches[0].clientX : event.clientX
      const clientY = event.touches ? event.touches[0].clientY : event.clientY
      
      // 获取游戏区域的边界
      const gameArea = document.querySelector('.game-area')
      if (!gameArea) return
      
      const gameAreaRect = gameArea.getBoundingClientRect()
      
      // 计算新位置（相对于游戏区域）
      let newX = clientX - gameAreaRect.left - this.dragOffset.x
      let newY = clientY - gameAreaRect.top - this.dragOffset.y
      
      // 限制在游戏区域内
      const cardWidth = 120
      const cardHeight = 80
      const padding = 20
      
      newX = Math.max(padding, Math.min(newX, gameAreaRect.width - cardWidth - padding))
      newY = Math.max(padding, Math.min(newY, gameAreaRect.height - cardHeight - padding))
      
      // 更新词卡位置
      this.wordCards[this.dragCardIndex].position = { x: newX, y: newY }
    },
    
    // 结束拖拽
    endDrag(event) {
      if (!this.isDragging || this.dragCardIndex === -1) return
      
      // 重置拖拽状态
      this.wordCards[this.dragCardIndex].isDragging = false
      this.isDragging = false
      this.dragCardIndex = -1
      this.dragStartPos = { x: 0, y: 0 }
      this.dragOffset = { x: 0, y: 0 }
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
  cursor: move;
  transition: transform 0.2s, box-shadow 0.2s, left 0.3s ease-out, top 0.3s ease-out;
  font-size: 14px;
  text-align: center;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
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

.word-card.dragging {
  z-index: 1000;
  transform: scale(1.05);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
  transition: none;
}

/* 爆炸碎片覆盖层 */
.explosion-fragments {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
}

.fragment {
  position: absolute;
  width: 33.33%;
  height: 33.33%;
  border-radius: 4px;
  opacity: 1;
  animation: fragment-scatter 0.6s ease-out forwards;
}

/* 9个碎片的位置布局（3x3网格） */
.fragment-1 { top: 0; left: 0; animation-delay: 0s; }
.fragment-2 { top: 0; left: 33.33%; animation-delay: 0.02s; }
.fragment-3 { top: 0; left: 66.66%; animation-delay: 0.04s; }
.fragment-4 { top: 33.33%; left: 0; animation-delay: 0.01s; }
.fragment-5 { top: 33.33%; left: 33.33%; animation-delay: 0.03s; }
.fragment-6 { top: 33.33%; left: 66.66%; animation-delay: 0.02s; }
.fragment-7 { top: 66.66%; left: 0; animation-delay: 0.01s; }
.fragment-8 { top: 66.66%; left: 33.33%; animation-delay: 0.03s; }
.fragment-9 { top: 66.66%; left: 66.66%; animation-delay: 0s; }

/* 原始卡片在爆炸时立即隐藏 */
.word-card.exploding {
  background: transparent !important;
}

.word-card.exploding .difficulty-label,
.word-card.exploding .english-word,
.word-card.exploding .chinese-word {
  opacity: 0;
}

/* 碎片四散动画 */
@keyframes fragment-scatter {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(var(--scatter-x, 0), var(--scatter-y, 0)) rotate(var(--scatter-rotate, 0deg)) scale(0.2);
    opacity: 0;
  }
}

/* 为每个碎片设置不同的随机飞散方向 */
.fragment-1 { --scatter-x: -150px; --scatter-y: -120px; --scatter-rotate: -75deg; }
.fragment-2 { --scatter-x: 20px; --scatter-y: -140px; --scatter-rotate: 25deg; }
.fragment-3 { --scatter-x: 160px; --scatter-y: -95px; --scatter-rotate: 85deg; }
.fragment-4 { --scatter-x: -135px; --scatter-y: 15px; --scatter-rotate: -50deg; }
.fragment-5 { --scatter-x: -30px; --scatter-y: -20px; --scatter-rotate: 200deg; }
.fragment-6 { --scatter-x: 145px; --scatter-y: 25px; --scatter-rotate: 110deg; }
.fragment-7 { --scatter-x: -110px; --scatter-y: 130px; --scatter-rotate: -80deg; }
.fragment-8 { --scatter-x: 35px; --scatter-y: 155px; --scatter-rotate: 45deg; }
.fragment-9 { --scatter-x: 170px; --scatter-y: 125px; --scatter-rotate: 150deg; }

/* 加分提示样式 */
.score-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 24px;
  font-weight: bold;
  color: #FFD700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  z-index: 20;
  pointer-events: none;
  animation: score-popup-animation 1.2s ease-out forwards;
}

@keyframes score-popup-animation {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0;
  }
  20% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 1;
  }
  40% {
    transform: translate(-50%, -60%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -80%) scale(0.8);
    opacity: 0;
  }
}

/* 错误输入反馈动画 */
.word-input.error-shake {
  animation: shake 0.6s ease-in-out;
  border: 2px solid #ff4757;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
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
  caret-color: transparent;
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

.key-btn:active,
.key-btn.key-pressed {
  transform: translateY(2px);
  background: #007bff;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
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