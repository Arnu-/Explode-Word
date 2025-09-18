<template>
  <div class="game-panel">
    <!-- 加载状态遮罩层 -->
    <div v-if="isLoadingWords" class="loading-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载单词数据...</div>
      </div>
    </div>

    <!-- 错误状态遮罩层 -->
    <div v-if="loadError" class="error-overlay">
      <div class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-text">{{ loadError }}</div>
        <button class="retry-btn" @click="initializeGame">重试</button>
        <button class="back-btn" @click="$router.push({ name: 'levels' })">返回关卡选择</button>
      </div>
    </div>

    <!-- 模式选择遮罩层 -->
    <div v-if="showModeSelection && !isLoadingWords && !loadError" class="mode-selection-overlay">
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
    <div class="game-content">
      <!-- 左侧统计面板 -->
      <aside class="stats-panel">
        <!-- 挑战模式显示得分 -->
        <div v-if="gameMode === 'challenge'" class="stat-item">
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
          <span class="stat-label">正确：</span>
          <span class="stat-value">{{ correctCount }}次</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">错误：</span>
          <span class="stat-value">{{ errors }}次</span>
        </div>
        <!-- 挑战模式显示连击数 -->
        <div v-if="gameMode === 'challenge'" class="stat-item">
          <span class="stat-label">连击：</span>
          <span class="stat-value combo-value" :class="getComboClass()">{{ consecutiveCorrect }}</span>
        </div>
        
        <!-- 游戏控制按钮 -->
        <div class="game-controls">
          <button class="control-btn pause-btn" @click="pauseGame">
            <svg v-if="!isGamePaused" width="16" height="16" viewBox="0 0 24 24" fill="none">
              <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
              <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
              <polygon points="5,3 19,12 5,21" fill="currentColor"/>
            </svg>
            {{ isGamePaused ? '继续' : '暂停' }}
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
        <!-- 连击奖励浮动提示 -->
        <div v-if="showComboEffect" class="combo-effect-overlay">
          <div class="combo-effect-popup" :class="comboEffectClass">
            <div class="combo-text">{{ comboEffectText }}</div>
            <div class="combo-bonus">+{{ comboEffectBonus }}分</div>
          </div>
        </div>
        
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
              
              <!-- 加分提示（仅挑战模式显示） -->
              <div v-if="gameMode === 'challenge'" class="score-popup">
                +{{ calculateWordScore(word.english) }}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- 游戏结束弹窗 -->
    <div v-if="showGameEndModal" class="game-end-overlay">
      <div class="game-end-container">
        <div class="game-end-header">
          <h2 class="game-end-title">🎉 游戏结束！</h2>
          <div class="game-mode-badge" :class="gameMode">
            {{ gameMode === 'training' ? '训练模式' : '挑战模式' }}
          </div>
        </div>
        
        <div class="game-results">
          <div class="result-item" v-if="gameMode === 'challenge'">
            <span class="result-label">最终得分</span>
            <span class="result-value score-value">{{ score }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">游戏用时</span>
            <span class="result-value">{{ formatTime(timeUsed) }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">正确次数</span>
            <span class="result-value correct-value">{{ correctCount }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">错误次数</span>
            <span class="result-value error-value">{{ errors }}</span>
          </div>
          <div class="result-item" v-if="gameMode === 'challenge' && maxConsecutiveCorrect > 0">
            <span class="result-label">最高连击</span>
            <span class="result-value combo-value">{{ maxConsecutiveCorrect }}</span>
          </div>
        </div>
        
        <div class="game-end-actions">
          <button class="action-btn next-level-btn" @click="goToNextLevel">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            下一关
          </button>
          <button class="action-btn select-level-btn" @click="goToLevelSelection">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="3" width="7" height="7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="14" y="3" width="7" height="7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="14" y="14" width="7" height="7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="3" y="14" width="7" height="7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            选择关卡
          </button>
          <button class="action-btn exit-btn" @click="exitToHome">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            退出游戏
          </button>
        </div>
      </div>
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
            :class="{ 
              'key-pressed': isKeyPressed(key),
              'key-highlighted': isKeyHighlighted(key),
              'key-shake': isKeyShaking(key)
            }"
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
            :class="{ 
              'key-pressed': isKeyPressed(key),
              'key-highlighted': isKeyHighlighted(key),
              'key-shake': isKeyShaking(key)
            }"
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
            :class="{ 
              'key-pressed': isKeyPressed(key),
              'key-highlighted': isKeyHighlighted(key),
              'key-shake': isKeyShaking(key),
              'space-key': key === '空格'
            }"
            @click="inputKey(key)"
          >
            {{ key }}
          </button>
        </div>
      </div>
    </footer>

    <!-- 底部导航栏 -->
    <nav class="bottom-nav">
      <div class="nav-item" @click="$router.push({ name: 'wordblast' })">
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
      <div class="nav-item" @click="$router.push({ name: 'profile' })">
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
import vocabularyGameService from '@/services/vocabularyGameService.js'
import { useRoute } from 'vue-router'

export default {
  name: 'GamePanel',
  props: {
    levelId: {
      type: [String, Number],
      default: 1
    }
  },
  setup() {
    const route = useRoute()
    return { route }
  },
  data() {
    return {
      showModeSelection: true,
      gameMode: null, // 'training' 或 'challenge'
      score: 0,
      timeUsed: 0, // 秒
      remainingWords: 10,
      errors: 0,
      correctCount: 0, // 正确次数
      consecutiveCorrect: 0, // 连续正确次数
      helpCount: 3,
      currentInput: '',
      
      // 帮助功能相关
      isHelpActive: false, // 是否正在使用帮助
      helpTargetWord: null, // 帮助目标单词
      helpCurrentLetterIndex: 0, // 当前应该输入的字母索引
      highlightedKey: '', // 当前高亮的按键
      shakingKey: '', // 当前晃动的按键
      shakeTimer: null, // 晃动定时器
      inputPlaceholder: '',
      gameConfig: getGameConfig(),
      gameTimer: null, // 游戏计时器
      isGamePaused: false, // 游戏是否暂停
      
      // 游戏会话相关
      gameSession: null,
      sessionCode: null,
      libraryId: null,
      groupId: null,
      levelTitle: '',
      
      // 数据加载状态
      isLoadingWords: false,
      loadError: null,
      
      // 连击效果相关
      showComboEffect: false,
      comboEffectText: '',
      comboEffectBonus: 0,
      comboEffectClass: '',
      
      // 游戏结束弹窗
      showGameEndModal: false,
      maxConsecutiveCorrect: 0, // 最高连击数
      
      // 虚拟键盘布局
      keyboardRow1: ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
      keyboardRow2: ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
      keyboardRow3: ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '空格'],
      
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
      wordCards: []
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
    
    // 初始化游戏数据
    this.initializeGame()
    
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
    
    // 停止游戏计时器
    this.stopGameTimer()
    
    // 清除帮助状态
    this.clearHelpState()
    
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
    
    // 检查按键是否被高亮（帮助功能）
    isKeyHighlighted(key) {
      return this.isHelpActive && this.highlightedKey === key
    },
    
    // 检查按键是否在晃动（帮助功能）
    isKeyShaking(key) {
      return this.shakingKey === key
    },
    
    // 处理输入框键盘事件
    handleInputKeyDown(event) {
      const key = event.key.toUpperCase()
      
      // 处理字母键
      if (key.match(/^[A-Z]$/)) {
        this.pressedKeys.add(key)
        // 阻止默认输入，我们手动控制
        event.preventDefault()
        
        // 如果正在使用帮助功能，验证输入
        if (this.isHelpActive && this.helpTargetWord) {
          const expectedLetter = this.helpTargetWord.english[this.helpCurrentLetterIndex].toUpperCase()
          
          if (key === expectedLetter) {
            // 输入正确，添加到输入框
            this.currentInput += key
            this.helpCurrentLetterIndex++
            
            // 检查是否完成了整个单词
            if (this.helpCurrentLetterIndex >= this.helpTargetWord.english.length) {
              // 完成帮助，清除帮助状态
              this.clearHelpState()
            } else {
              // 高亮下一个字母
              this.highlightNextLetter()
            }
          } else {
            // 输入错误，晃动正确的按键
            this.shakeWrongKey(expectedLetter)
            console.log('帮助模式：输入错误，期望', expectedLetter, '实际输入', key)
          }
        } else {
          // 非帮助模式，正常输入
          this.currentInput += key
        }
      }
      
      // 处理空格键
      if (event.key === ' ') {
        // 帮助模式下不允许空格
        if (this.isHelpActive) {
          event.preventDefault()
          return
        }
        // 允许空格输入
        return
      }
      
      // 处理退格键
      if (event.key === 'Backspace') {
        // 帮助模式下处理退格
        if (this.isHelpActive && this.helpCurrentLetterIndex > 0) {
          this.helpCurrentLetterIndex--
          this.highlightNextLetter()
        }
        // 允许默认的退格行为
        return
      }
      
      // 阻止其他非字母字符的输入（但允许空格）
      if (!key.match(/^[A-Z]$/) && event.key !== 'Backspace' && event.key !== 'Enter' && event.key !== ' ') {
        event.preventDefault()
      }
    },
    
    // 处理输入变化，确保只有大写字母和空格
    handleInputChange(event) {
      this.currentInput = event.target.value.toUpperCase().replace(/[^A-Z ]/g, '')
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
    // 初始化游戏
    async initializeGame() {
      try {
        // 从URL参数获取游戏信息
        this.libraryId = this.route.query.libraryId
        this.groupId = this.route.query.groupId
        this.levelTitle = this.route.query.levelTitle || '词汇挑战'
        
        if (!this.libraryId || !this.groupId) {
          console.error('缺少必要的游戏参数')
          this.loadError = '缺少必要的游戏参数'
          return
        }
        
        // 开始游戏会话
        await this.startGameSession()
        
      } catch (error) {
        console.error('初始化游戏失败:', error)
        this.loadError = '初始化游戏失败: ' + error.message
      }
    },
    
    // 开始游戏会话
    async startGameSession() {
      try {
        this.isLoadingWords = true
        
        const response = await vocabularyGameService.startGame(
          parseInt(this.libraryId),
          parseInt(this.groupId)
        )
        
        if (response && response.session_code) {
          this.sessionCode = response.session_code
          this.gameSession = response.session
          
          // 加载单词数据
          await this.loadGameWords()
        } else {
          throw new Error('无效的游戏会话响应')
        }
        
      } catch (error) {
        console.error('开始游戏会话失败:', error)
        this.loadError = '开始游戏失败: ' + error.message
      } finally {
        this.isLoadingWords = false
      }
    },
    
    // 加载游戏单词
    async loadGameWords() {
      try {
        const response = await vocabularyGameService.getGameWords(this.sessionCode)
        
        if (response && response.words) {
          // 转换单词数据为游戏卡片格式
          this.wordCards = response.words.map((word, index) => ({
            id: word.id,
            english: word.english,
            chinese: word.chinese,
            difficulty: word.difficulty_level || 1,
            completed: false,
            exploding: false,
            position: { x: 0, y: 0 }, // 稍后生成随机位置
            isDragging: false
          }))
          
          // 更新剩余单词数
          this.remainingWords = this.wordCards.length
          
          // 计算帮助次数：单词数量的十分之一，最低3次
          this.helpCount = Math.max(3, Math.floor(this.wordCards.length / 10))
          
          // 生成随机位置
          this.generateRandomPositions()
          
          console.log('加载了', this.wordCards.length, '个单词，帮助次数：', this.helpCount)
        } else {
          throw new Error('无效的单词数据响应')
        }
        
      } catch (error) {
        console.error('加载单词数据失败:', error)
        this.loadError = '加载单词失败: ' + error.message
      }
    },

    selectMode(mode) {
      this.gameMode = mode
      this.showModeSelection = false
      
      // 重置游戏状态
      this.resetGameState()
      
      // 开始计时
      this.startGameTimer()
      
      console.log('选择模式:', mode)
    },
    
    // 重置游戏状态
    resetGameState() {
      this.score = 0
      this.timeUsed = 0
      this.errors = 0
      this.correctCount = 0
      this.consecutiveCorrect = 0
      this.remainingWords = this.wordCards.length
      this.isGamePaused = false
      this.currentInput = ''
      
      // 清除帮助状态
      this.clearHelpState()
      
      // 重置所有词卡状态
      this.wordCards.forEach(card => {
        card.completed = false
        card.exploding = false
        card.isDragging = false
      })
    },
    
    // 开始游戏计时器
    startGameTimer() {
      if (this.gameTimer) {
        clearInterval(this.gameTimer)
      }
      
      this.gameTimer = setInterval(() => {
        if (!this.isGamePaused) {
          this.timeUsed++
        }
      }, 1000)
    },
    
    // 停止游戏计时器
    stopGameTimer() {
      if (this.gameTimer) {
        clearInterval(this.gameTimer)
        this.gameTimer = null
      }
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
      // 处理空格键
      if (key === '空格') {
        // 帮助模式下不允许空格
        if (this.isHelpActive) {
          return
        }
        this.currentInput += ' '
      } else {
        // 如果正在使用帮助功能，验证输入
        if (this.isHelpActive && this.helpTargetWord) {
          const expectedLetter = this.helpTargetWord.english[this.helpCurrentLetterIndex].toUpperCase()
          
          if (key === expectedLetter) {
            // 输入正确，添加到输入框
            this.currentInput += key
            this.helpCurrentLetterIndex++
            
            // 检查是否完成了整个单词
            if (this.helpCurrentLetterIndex >= this.helpTargetWord.english.length) {
              // 完成帮助，清除帮助状态
              this.clearHelpState()
            } else {
              // 高亮下一个字母
              this.highlightNextLetter()
            }
          } else {
            // 输入错误，晃动正确的按键
            this.shakeWrongKey(expectedLetter)
            console.log('帮助模式：输入错误，期望', expectedLetter, '实际输入', key)
          }
        } else {
          // 非帮助模式，正常输入
          this.currentInput += key
        }
      }
      
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
    
    async submitWord() {
      if (!this.currentInput.trim()) return
      
      const inputWord = this.currentInput.trim().toLowerCase()
      console.log('提交单词:', inputWord)
      
      // 查找匹配的单词卡片
      const matchedCardIndex = this.wordCards.findIndex(card => 
        !card.completed && card.english.toLowerCase() === inputWord
      )
      
      const isCorrect = matchedCardIndex !== -1
      let matchedCard = null
      let wordId = null
      
      if (isCorrect) {
        matchedCard = this.wordCards[matchedCardIndex]
        wordId = matchedCard.id
        
        // 标记为完成状态，触发炸开动画
        this.wordCards[matchedCardIndex] = {
          ...matchedCard,
          completed: true,
          exploding: true
        }
        
        // 更新统计
        this.correctCount++
        this.consecutiveCorrect++
        this.remainingWords--
        
        // 更新最高连击记录
        if (this.consecutiveCorrect > this.maxConsecutiveCorrect) {
          this.maxConsecutiveCorrect = this.consecutiveCorrect
        }
        
        // 计算得分（仅在挑战模式）
        if (this.gameMode === 'challenge') {
          const baseScore = this.calculateWordScore(matchedCard.english)
          let totalScore = baseScore
          
          // 检查连击奖励
          const comboBonus = this.getComboBonus(this.consecutiveCorrect)
          if (comboBonus > 0) {
            totalScore += comboBonus
            this.showComboBonusEffect(comboBonus)
          }
          
          this.score += totalScore
          console.log(`单词正确！基础得分: ${baseScore}, 连击奖励: ${comboBonus}, 总得分: ${totalScore}`)
        }
        
        // 延迟移除卡片（等待动画完成）
        setTimeout(() => {
          this.wordCards.splice(matchedCardIndex, 1)
          
          // 检查游戏是否结束
          if (this.wordCards.length === 0) {
            this.gameComplete()
          }
        }, 800)
        
      } else {
        // 单词错误
        this.errors++
        this.consecutiveCorrect = 0 // 重置连击
        
        // 挑战模式扣分
        if (this.gameMode === 'challenge') {
          // 找到最可能的单词进行扣分计算（这里简化处理，可以改进）
          const avgWordLength = Math.round(this.wordCards.reduce((sum, card) => sum + card.english.length, 0) / this.wordCards.length)
          const penalty = this.calculateScorePenalty(avgWordLength)
          this.score = Math.max(0, this.score - penalty)
          console.log(`单词错误！扣分: ${penalty}`)
        }
        
        // 显示错误反馈
        this.showErrorFeedback()
      }
      
      // 提交答案到服务器（如果有游戏会话）
      if (this.sessionCode) {
        try {
          await vocabularyGameService.submitAnswer(this.sessionCode, {
            word_id: wordId || (this.wordCards.length > 0 ? this.wordCards[0].id : null),
            answer: inputWord,
            is_correct: isCorrect,
            time_used: 5 // 可以记录实际用时
          })
        } catch (error) {
          console.error('提交答案失败:', error)
          // 不影响游戏继续进行
        }
      }
      
      // 清空输入
      this.currentInput = ''
      
      // 如果提交的是帮助目标单词，清除帮助状态
      if (this.isHelpActive && matchedCard && matchedCard.id === this.helpTargetWord?.id) {
        this.clearHelpState()
      }
    },
    
    // 计算单词得分（字母个数）
    calculateWordScore(word) {
      return word.length
    },
    
    // 计算错误扣分（字母个数的一半，单数则减一再除以2）
    calculateScorePenalty(wordLength) {
      if (wordLength % 2 === 0) {
        return Math.floor(wordLength / 2)
      } else {
        return Math.floor((wordLength - 1) / 2)
      }
    },
    
    // 获取连击奖励
    getComboBonus(consecutiveCount) {
      if (consecutiveCount === 8) {
        return 8
      } else if (consecutiveCount === 5) {
        return 5
      } else if (consecutiveCount === 3) {
        return 3
      }
      return 0
    },
    
    // 显示连击奖励效果
    showComboBonusEffect(bonus) {
      // 设置连击效果文本和样式
      if (bonus === 3) {
        this.comboEffectText = '三连对！'
        this.comboEffectClass = 'combo-effect-rare'
      } else if (bonus === 5) {
        this.comboEffectText = '五连对！'
        this.comboEffectClass = 'combo-effect-epic'
      } else if (bonus === 8) {
        this.comboEffectText = '八连对！'
        this.comboEffectClass = 'combo-effect-legendary'
      }
      
      this.comboEffectBonus = bonus
      this.showComboEffect = true
      
      // 2秒后隐藏效果
      setTimeout(() => {
        this.showComboEffect = false
        this.comboEffectText = ''
        this.comboEffectBonus = 0
        this.comboEffectClass = ''
      }, 2000)
      
      console.log(`连击奖励！${this.comboEffectText}+${bonus}分`)
    },
    
    // 游戏完成
    async gameComplete() {
      this.stopGameTimer()
      
      // 结束游戏会话（如果有）
      if (this.sessionCode) {
        try {
          await vocabularyGameService.finishGame(this.sessionCode)
          console.log('游戏会话已结束')
        } catch (error) {
          console.error('结束游戏会话失败:', error)
        }
      }
      
      this.showGameEndModal = true
      console.log('游戏完成！')
    },
    
    // 下一关
    goToNextLevel() {
      const nextLevelId = parseInt(this.levelId) + 1
      this.$router.push({ 
        name: 'game', 
        params: { levelId: nextLevelId }
      })
    },
    
    // 选择关卡
    goToLevelSelection() {
      this.$router.push({ name: 'levels' })
    },
    
    // 退出到首页
    exitToHome() {
      this.$router.push({ name: 'wordblast' })
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
      if (this.helpCount > 0 && !this.isHelpActive) {
        this.helpCount--
        
        // 随机选择一个未完成的单词
        const availableWords = this.wordCards.filter(card => !card.completed && !card.exploding)
        if (availableWords.length === 0) {
          console.log('没有可用的单词进行帮助')
          return
        }
        
        // 随机选择一个单词
        const randomIndex = Math.floor(Math.random() * availableWords.length)
        this.helpTargetWord = availableWords[randomIndex]
        
        // 激活帮助模式
        this.isHelpActive = true
        this.helpCurrentLetterIndex = 0
        
        // 高亮目标单词
        this.highlightHelpWord()
        
        // 高亮第一个字母
        this.highlightNextLetter()
        
        console.log('使用帮助，目标单词：', this.helpTargetWord.english)
      }
    },
    
    // 高亮帮助目标单词
    highlightHelpWord() {
      if (!this.helpTargetWord) return
      
      // 找到目标单词在数组中的索引
      const wordIndex = this.wordCards.findIndex(card => card.id === this.helpTargetWord.id)
      if (wordIndex !== -1) {
        // 添加高亮样式类
        this.$nextTick(() => {
          const wordElement = document.querySelectorAll('.word-card')[wordIndex]
          if (wordElement) {
            wordElement.classList.add('help-highlighted')
          }
        })
      }
    },
    
    // 高亮下一个应该输入的字母
    highlightNextLetter() {
      if (!this.helpTargetWord || this.helpCurrentLetterIndex >= this.helpTargetWord.english.length) {
        return
      }
      
      const nextLetter = this.helpTargetWord.english[this.helpCurrentLetterIndex].toUpperCase()
      this.highlightedKey = nextLetter
      
      console.log('高亮字母：', nextLetter, '位置：', this.helpCurrentLetterIndex)
    },
    
    // 清除帮助状态
    clearHelpState() {
      this.isHelpActive = false
      this.helpTargetWord = null
      this.helpCurrentLetterIndex = 0
      this.highlightedKey = ''
      this.shakingKey = ''
      
      // 清除单词高亮
      document.querySelectorAll('.word-card.help-highlighted').forEach(element => {
        element.classList.remove('help-highlighted')
      })
      
      // 清除晃动定时器
      if (this.shakeTimer) {
        clearTimeout(this.shakeTimer)
        this.shakeTimer = null
      }
    },
    
    // 晃动错误的按键
    shakeWrongKey(correctKey) {
      this.shakingKey = correctKey
      
      // 清除之前的定时器
      if (this.shakeTimer) {
        clearTimeout(this.shakeTimer)
      }
      
      // 设置晃动持续时间
      this.shakeTimer = setTimeout(() => {
        this.shakingKey = ''
        this.shakeTimer = null
      }, 600)
    },
    
    pauseGame() {
      this.isGamePaused = !this.isGamePaused
      console.log(this.isGamePaused ? '游戏暂停' : '游戏继续')
    },
    
    exitGame() {
      this.stopGameTimer()
      console.log('退出游戏')
      this.$router.push({ name: 'levels' })
    },
    
    // 获取连击样式类
    getComboClass() {
      if (this.consecutiveCorrect >= 8) {
        return 'combo-legendary'
      } else if (this.consecutiveCorrect >= 5) {
        return 'combo-epic'
      } else if (this.consecutiveCorrect >= 3) {
        return 'combo-rare'
      }
      return ''
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

/* 加载状态遮罩层 */
.loading-overlay {
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

.loading-container {
  text-align: center;
  color: white;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
}

/* 错误状态遮罩层 */
.error-overlay {
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

.error-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 400px;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.error-text {
  color: white;
  font-size: 16px;
  margin-bottom: 30px;
  line-height: 1.5;
}

.retry-btn, .back-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  margin: 0 10px;
  transition: background-color 0.2s;
}

.retry-btn:hover, .back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
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

/* 连击数值样式 */
.combo-value {
  transition: all 0.3s ease;
}

.combo-value.combo-rare {
  color: #55efc4;
  text-shadow: 0 0 10px rgba(85, 239, 196, 0.5);
  animation: combo-glow 1s ease-in-out infinite alternate;
}

.combo-value.combo-epic {
  color: #fdcb6e;
  text-shadow: 0 0 15px rgba(253, 203, 110, 0.7);
  animation: combo-glow 0.8s ease-in-out infinite alternate;
}

.combo-value.combo-legendary {
  color: #fd79a8;
  text-shadow: 0 0 20px rgba(253, 121, 168, 0.9);
  animation: combo-glow 0.6s ease-in-out infinite alternate;
  transform: scale(1.1);
}

@keyframes combo-glow {
  0% {
    text-shadow: 0 0 5px currentColor;
  }
  100% {
    text-shadow: 0 0 20px currentColor, 0 0 30px currentColor;
  }
}

/* 连击效果浮动提示 */
.combo-effect-overlay {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  pointer-events: none;
}

.combo-effect-popup {
  background: rgba(0, 0, 0, 0.9);
  border-radius: 20px;
  padding: 20px 30px;
  text-align: center;
  backdrop-filter: blur(10px);
  border: 2px solid;
  animation: combo-popup-animation 2s ease-out forwards;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.combo-effect-rare {
  border-color: #55efc4;
  box-shadow: 0 10px 30px rgba(85, 239, 196, 0.4);
}

.combo-effect-epic {
  border-color: #fdcb6e;
  box-shadow: 0 10px 30px rgba(253, 203, 110, 0.4);
}

.combo-effect-legendary {
  border-color: #fd79a8;
  box-shadow: 0 10px 30px rgba(253, 121, 168, 0.4);
}

.combo-text {
  font-size: 24px;
  font-weight: bold;
  color: white;
  margin-bottom: 8px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.combo-bonus {
  font-size: 20px;
  font-weight: bold;
  color: #FFD700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.combo-effect-rare .combo-text {
  color: #55efc4;
  text-shadow: 0 0 10px rgba(85, 239, 196, 0.8);
}

.combo-effect-epic .combo-text {
  color: #fdcb6e;
  text-shadow: 0 0 15px rgba(253, 203, 110, 0.8);
}

.combo-effect-legendary .combo-text {
  color: #fd79a8;
  text-shadow: 0 0 20px rgba(253, 121, 168, 0.8);
}

@keyframes combo-popup-animation {
  0% {
    transform: translateX(-50%) translateY(-20px) scale(0.5);
    opacity: 0;
  }
  15% {
    transform: translateX(-50%) translateY(0) scale(1.2);
    opacity: 1;
  }
  30% {
    transform: translateX(-50%) translateY(0) scale(1);
    opacity: 1;
  }
  85% {
    transform: translateX(-50%) translateY(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateX(-50%) translateY(-10px) scale(0.8);
    opacity: 0;
  }
}

/* 游戏结束弹窗样式 */
.game-end-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(10px);
  animation: modal-fade-in 0.3s ease-out;
}

.game-end-container {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 24px;
  padding: 40px;
  text-align: center;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  max-width: 500px;
  width: 90%;
  animation: modal-slide-up 0.4s ease-out;
}

.game-end-header {
  margin-bottom: 30px;
}

.game-end-title {
  font-size: 32px;
  font-weight: bold;
  color: white;
  margin-bottom: 15px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.game-mode-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.game-mode-badge.training {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
}

.game-mode-badge.challenge {
  background: linear-gradient(135deg, #fd79a8, #e84393);
}

.game-results {
  margin-bottom: 40px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  margin-bottom: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.result-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.result-value {
  font-size: 18px;
  font-weight: bold;
  color: white;
}

.score-value {
  color: #FFD700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.correct-value {
  color: #55efc4;
}

.error-value {
  color: #ff7675;
}

.combo-value {
  color: #fd79a8;
  text-shadow: 0 0 10px rgba(253, 121, 168, 0.5);
}

.game-end-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 15px 25px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  min-width: 140px;
}

.next-level-btn {
  background: linear-gradient(135deg, #55efc4, #00b894);
  box-shadow: 0 4px 15px rgba(85, 239, 196, 0.3);
}

.next-level-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(85, 239, 196, 0.4);
}

.select-level-btn {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
  box-shadow: 0 4px 15px rgba(116, 185, 255, 0.3);
}

.select-level-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(116, 185, 255, 0.4);
}

.action-btn.exit-btn {
  background: linear-gradient(135deg, #ff7675, #d63031);
  box-shadow: 0 4px 15px rgba(255, 118, 117, 0.3);
}

.action-btn.exit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 118, 117, 0.4);
}

@keyframes modal-fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modal-slide-up {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
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

.key-btn.space-key {
  width: 120px;
  background: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.key-btn.space-key:hover {
  background: rgba(255, 255, 255, 0.95);
}

.key-btn.space-key:active,
.key-btn.space-key.key-pressed {
  background: #28a745;
  color: white;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

/* 帮助功能样式 */
.key-btn.key-highlighted {
  background: #FFD700 !important;
  color: #000 !important;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
  animation: key-highlight-pulse 1.5s ease-in-out infinite;
  transform: scale(1.1);
}

.key-btn.key-shake {
  animation: key-shake 0.6s ease-in-out;
  background: #ff4757 !important;
  color: white !important;
}

@keyframes key-highlight-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
  }
  50% {
    box-shadow: 0 0 30px rgba(255, 215, 0, 1), 0 0 40px rgba(255, 215, 0, 0.6);
  }
}

@keyframes key-shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-3px); }
  20%, 40%, 60%, 80% { transform: translateX(3px); }
}

/* 帮助目标单词高亮 */
.word-card.help-highlighted {
  border: 3px solid #FFD700 !important;
  box-shadow: 0 0 25px rgba(255, 215, 0, 0.8) !important;
  animation: word-highlight-pulse 2s ease-in-out infinite;
  transform: scale(1.05) !important;
  z-index: 100;
}

@keyframes word-highlight-pulse {
  0%, 100% {
    border-color: #FFD700;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
  }
  50% {
    border-color: #FFA500;
    box-shadow: 0 0 35px rgba(255, 215, 0, 1), 0 0 45px rgba(255, 165, 0, 0.6);
  }
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
  
  /* 游戏结束弹窗响应式 */
  .game-end-container {
    padding: 30px 20px;
    max-width: 95%;
  }
  
  .game-end-title {
    font-size: 24px;
  }
  
  .game-end-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .action-btn {
    width: 100%;
    min-width: auto;
  }
  
  .result-item {
    padding: 12px 15px;
  }
  
  .result-label {
    font-size: 14px;
  }
  
  .result-value {
    font-size: 16px;
  }
}
</style>