<template>
  <div class="game-config">
    <!-- 左侧配置面板 -->
    <div class="config-panel">
      <div class="config-content">

        
        <!-- 英文设置 -->
        <div class="config-section">
          <h3 class="section-title">英文设置</h3>
          
          <div class="config-item">
            <label>英文字体大小</label>
            <input 
              type="range" 
              v-model.number="config.englishFontSize" 
              min="12" 
              max="32"
              class="config-slider"
            />
            <span class="slider-value">{{ config.englishFontSize }}px</span>
          </div>
          
          <div class="config-item">
            <label>英文字体颜色</label>
            <input 
              type="color" 
              v-model="config.englishColor" 
              class="config-color"
            />
            <span class="color-value">{{ config.englishColor }}</span>
          </div>
        </div>

        <!-- 中文设置 -->
        <div class="config-section">
          <h3 class="section-title">中文设置</h3>
          
          <div class="config-item">
            <label>中文字体大小</label>
            <input 
              type="range" 
              v-model.number="config.chineseFontSize" 
              min="10" 
              max="28"
              class="config-slider"
            />
            <span class="slider-value">{{ config.chineseFontSize }}px</span>
          </div>
          
          <div class="config-item">
            <label>中文字体颜色</label>
            <input 
              type="color" 
              v-model="config.chineseColor" 
              class="config-color"
            />
            <span class="color-value">{{ config.chineseColor }}</span>
          </div>
        </div>

        <!-- 词卡设置 -->
        <div class="config-section">
          <h3 class="section-title">词卡设置</h3>
          
          <div class="config-item">
            <label>词卡大小</label>
            <div class="size-options">
              <label class="radio-option">
                <input type="radio" v-model="config.cardSize" value="small" />
                <span>小</span>
              </label>
              <label class="radio-option">
                <input type="radio" v-model="config.cardSize" value="medium" />
                <span>中</span>
              </label>
              <label class="radio-option">
                <input type="radio" v-model="config.cardSize" value="large" />
                <span>大</span>
              </label>
            </div>
          </div>
          
          <div class="config-item">
            <label>词卡圆角</label>
            <input 
              type="range" 
              v-model.number="config.borderRadius" 
              min="0" 
              max="20"
              class="config-slider"
            />
            <span class="slider-value">{{ config.borderRadius }}px</span>
          </div>
        </div>

        <!-- 难度级别颜色设置 -->
        <div class="config-section">
          <h3 class="section-title">难度级别背景颜色</h3>
          
          <div class="config-item">
            <label>级别 1 背景颜色</label>
            <input 
              type="color" 
              v-model="config.levelColors.level1" 
              class="config-color"
            />
            <span class="color-value">{{ config.levelColors.level1 }}</span>
          </div>
          
          <div class="config-item">
            <label>级别 2 背景颜色</label>
            <input 
              type="color" 
              v-model="config.levelColors.level2" 
              class="config-color"
            />
            <span class="color-value">{{ config.levelColors.level2 }}</span>
          </div>
          
          <div class="config-item">
            <label>级别 3 背景颜色</label>
            <input 
              type="color" 
              v-model="config.levelColors.level3" 
              class="config-color"
            />
            <span class="color-value">{{ config.levelColors.level3 }}</span>
          </div>
          
          <div class="config-item">
            <label>级别 4 背景颜色</label>
            <input 
              type="color" 
              v-model="config.levelColors.level4" 
              class="config-color"
            />
            <span class="color-value">{{ config.levelColors.level4 }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="config-actions">
          <button @click="resetConfig" class="btn btn-secondary">重置默认</button>
          <button @click="saveConfig" class="btn btn-primary">保存设置</button>
        </div>
      </div>
    </div>

    <!-- 右侧预览面板 -->
    <div class="preview-panel">
      <div class="preview-content">
        <h3 class="preview-title">词卡预览</h3>
        
        <div class="card-previews">
          <!-- 级别 1 词卡预览 -->
          <div class="preview-item">
            <h4>级别 1 词卡</h4>
            <div 
              class="word-card level1"
              :style="getCardStyle('level1')"
            >
              <div class="word-english" :style="getEnglishStyle()">Apple</div>
              <div class="word-chinese" :style="getChineseStyle()">苹果</div>
            </div>
          </div>
          
          <!-- 级别 2 词卡预览 -->
          <div class="preview-item">
            <h4>级别 2 词卡</h4>
            <div 
              class="word-card level2"
              :style="getCardStyle('level2')"
            >
              <div class="word-english" :style="getEnglishStyle()">Beautiful</div>
              <div class="word-chinese" :style="getChineseStyle()">美丽的</div>
            </div>
          </div>
          
          <!-- 级别 3 词卡预览 -->
          <div class="preview-item">
            <h4>级别 3 词卡</h4>
            <div 
              class="word-card level3"
              :style="getCardStyle('level3')"
            >
              <div class="word-english" :style="getEnglishStyle()">Magnificent</div>
              <div class="word-chinese" :style="getChineseStyle()">壮丽的</div>
            </div>
          </div>
          
          <!-- 级别 4 词卡预览 -->
          <div class="preview-item">
            <h4>级别 4 词卡</h4>
            <div 
              class="word-card level4"
              :style="getCardStyle('level4')"
            >
              <div class="word-english" :style="getEnglishStyle()">Serendipitous</div>
              <div class="word-chinese" :style="getChineseStyle()">意外发现的</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameConfig',
  data() {
    return {
      config: {
        englishFontSize: 18,
        englishColor: '#2c3e50',
        chineseFontSize: 14,
        chineseColor: '#7f8c8d',
        cardSize: 'medium',
        borderRadius: 8,
        levelColors: {
          level1: '#4CAF50',
          level2: '#2196F3',
          level3: '#FF9800',
          level4: '#F44336'
        }
      }
    }
  },
  methods: {
    getCardStyle(level) {
      const sizeMap = {
        small: { width: '120px', height: '80px', padding: '8px' },
        medium: { width: '150px', height: '100px', padding: '12px' },
        large: { width: '180px', height: '120px', padding: '16px' }
      }
      
      const size = sizeMap[this.config.cardSize]
      
      return {
        backgroundColor: this.config.levelColors[level],
        borderRadius: `${this.config.borderRadius}px`,
        width: size.width,
        height: size.height,
        padding: size.padding,
        border: '2px solid #ddd'
      }
    },
    
    getEnglishStyle() {
      return {
        fontSize: `${this.config.englishFontSize}px`,
        color: this.config.englishColor
      }
    },
    
    getChineseStyle() {
      return {
        fontSize: `${this.config.chineseFontSize}px`,
        color: this.config.chineseColor
      }
    },
    
    saveConfig() {
      localStorage.setItem('gameConfig', JSON.stringify(this.config))
      alert('设置已保存！')
    },
    
    resetConfig() {
      this.config = {
        englishFontSize: 18,
        englishColor: '#2c3e50',
        chineseFontSize: 14,
        chineseColor: '#7f8c8d',
        cardSize: 'medium',
        borderRadius: 8,
        levelColors: {
          level1: '#4CAF50',
          level2: '#2196F3',
          level3: '#FF9800',
          level4: '#F44336'
        }
      }
    },
    
    loadConfig() {
      const saved = localStorage.getItem('gameConfig')
      if (saved) {
        this.config = { ...this.config, ...JSON.parse(saved) }
      }
    }
  },
  
  mounted() {
    this.loadConfig()
  }
}
</script>

<style scoped>
.game-config {
  display: flex;
  height: calc(100vh - 7rem); /* 减去顶部栏4rem + 底部栏3rem */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 左侧配置面板 */
.config-panel {
  width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  overflow-y: auto;
  max-height: calc(100vh - 7rem); /* 减去顶部栏4rem + 底部栏3rem */
}

.config-content {
  padding: 24px;
}

.config-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 24px;
  text-align: center;
}

.config-section {
  margin-bottom: 32px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #444;
  margin-bottom: 16px;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
}

.config-item {
  margin-bottom: 16px;
}

.config-item label {
  display: block;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

.config-slider {
  width: 60%;
  margin-right: 12px;
}

.slider-value {
  font-weight: 600;
  color: #667eea;
  min-width: 50px;
  display: inline-block;
}

.config-color {
  width: 60px;
  height: 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-right: 12px;
}

.color-value {
  font-family: monospace;
  font-size: 14px;
  color: #666;
  vertical-align: middle;
}

.size-options {
  display: flex;
  gap: 16px;
}

.radio-option {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-option input {
  width: auto;
}

.config-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5a6fd8;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f8f9fa;
  color: #666;
  border: 2px solid #e1e5e9;
}

.btn-secondary:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

/* 右侧预览面板 */
.preview-panel {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.preview-content {
  max-width: 600px;
  margin: 0 auto;
}

.preview-title {
  font-size: 24px;
  font-weight: bold;
  color: white;
  text-align: center;
  margin-bottom: 32px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.card-previews {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.preview-item {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.preview-item h4 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.word-card {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  cursor: pointer;
  user-select: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  gap: 4px;
  transition: transform 0.3s ease;
}

.word-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.word-english {
  font-weight: 600;
}

.word-chinese {
  font-weight: 500;
}

/* 滚动条样式 */
.config-panel::-webkit-scrollbar,
.preview-panel::-webkit-scrollbar {
  width: 8px;
}

.config-panel::-webkit-scrollbar-track,
.preview-panel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.config-panel::-webkit-scrollbar-thumb,
.preview-panel::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.config-panel::-webkit-scrollbar-thumb:hover,
.preview-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .game-config {
    flex-direction: column;
    height: calc(100vh - 7rem); /* 减去顶部栏4rem + 底部栏3rem */
  }
  
  .config-panel {
    width: 100%;
    max-height: calc(50vh - 3.5rem); /* 移动端时减少一半的顶部底部栏高度 */
  }
  
  .card-previews {
    grid-template-columns: 1fr;
  }
}
</style>