<template>
  <div class="settings-page">
    <div class="page-overlay"></div>
    
    <div class="settings-container content-layer">

      
      <div class="settings-content">
        <!-- 音效设置 -->
        <div class="setting-section">
          <h3 class="section-title">音效设置</h3>
          <div class="setting-item">
            <label class="setting-label">背景音乐</label>
            <div class="setting-control">
              <input type="range" v-model="settings.bgmVolume" min="0" max="100" class="volume-slider">
              <span class="volume-value">{{ settings.bgmVolume }}%</span>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">音效</label>
            <div class="setting-control">
              <input type="range" v-model="settings.sfxVolume" min="0" max="100" class="volume-slider">
              <span class="volume-value">{{ settings.sfxVolume }}%</span>
            </div>
          </div>
        </div>
        
        <!-- 游戏设置 -->
        <div class="setting-section">
          <h3 class="section-title">游戏设置</h3>
          <div class="setting-item">
            <label class="setting-label">自动保存进度</label>
            <div class="setting-control">
              <label class="toggle-switch">
                <input type="checkbox" v-model="settings.autoSave">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">显示提示</label>
            <div class="setting-control">
              <label class="toggle-switch">
                <input type="checkbox" v-model="settings.showHints">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">难度级别</label>
            <div class="setting-control">
              <select v-model="settings.difficulty" class="difficulty-select">
                <option value="easy">简单</option>
                <option value="normal">普通</option>
                <option value="hard">困难</option>
                <option value="expert">专家</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- 显示设置 -->
        <div class="setting-section">
          <h3 class="section-title">显示设置</h3>
          <div class="setting-item">
            <label class="setting-label">动画效果</label>
            <div class="setting-control">
              <label class="toggle-switch">
                <input type="checkbox" v-model="settings.animations">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">粒子效果</label>
            <div class="setting-control">
              <label class="toggle-switch">
                <input type="checkbox" v-model="settings.particles">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="settings-actions">
          <button @click="resetSettings" class="reset-btn">
            <i class="fa-solid fa-rotate-left"></i>
            恢复默认
          </button>
          <button @click="saveSettings" class="save-btn">
            <i class="fa-solid fa-floppy-disk"></i>
            保存设置
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 设置数据
const settings = ref({
  bgmVolume: 70,
  sfxVolume: 80,
  autoSave: true,
  showHints: true,
  difficulty: 'normal',
  animations: true,
  particles: true
})

// 默认设置
const defaultSettings = {
  bgmVolume: 70,
  sfxVolume: 80,
  autoSave: true,
  showHints: true,
  difficulty: 'normal',
  animations: true,
  particles: true
}

// 加载设置
const loadSettings = () => {
  const savedSettings = localStorage.getItem('gameSettings')
  if (savedSettings) {
    try {
      settings.value = { ...defaultSettings, ...JSON.parse(savedSettings) }
    } catch (error) {
      console.error('加载设置失败:', error)
      settings.value = { ...defaultSettings }
    }
  }
}

// 保存设置
const saveSettings = () => {
  try {
    localStorage.setItem('gameSettings', JSON.stringify(settings.value))
    // 这里可以添加保存成功的提示
    console.log('设置已保存')
  } catch (error) {
    console.error('保存设置失败:', error)
  }
}

// 重置设置
const resetSettings = () => {
  settings.value = { ...defaultSettings }
  saveSettings()
}

// 组件挂载时加载设置
onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
@import '@/assets/theme.css';

.settings-page {
  min-height: 100vh;
  color: var(--color-text-primary);
  position: relative;
  padding: 2rem;
  overflow: hidden;
}

.page-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
  z-index: 0;
  border-radius: var(--border-radius-large);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.1);
}

.content-layer {
  position: relative;
  z-index: 1;
}

.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

.settings-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.setting-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  color: #ffffff;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  font-size: 1rem;
  font-weight: 500;
  color: #e2e8f0;
}

.setting-control {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.volume-slider {
  width: 120px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 50%;
  cursor: pointer;
}

.volume-value {
  font-size: 0.875rem;
  color: #cbd5e1;
  min-width: 40px;
  text-align: right;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.2);
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.difficulty-select {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  outline: none;
  cursor: pointer;
}

.difficulty-select option {
  background: #1e1b4b;
  color: white;
}

.settings-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.reset-btn, .save-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.reset-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.reset-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: translateY(-2px);
}

.save-btn {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
}

@media (max-width: 768px) {
  .settings-page {
    padding: 1rem;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .setting-control {
    width: 100%;
    justify-content: flex-end;
  }
  
  .settings-actions {
    flex-direction: column;
  }
}
</style>