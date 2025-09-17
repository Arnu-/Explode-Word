<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>选择词库</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <div class="modal-body">
        <div v-if="loading" class="loading-container">
          <div class="loading-text">加载词库中...</div>
        </div>

        <div v-else-if="error" class="error-container">
          <div class="error-text">{{ error }}</div>
          <button @click="loadLibraries" class="retry-button">重试</button>
        </div>

        <div v-else-if="libraries.length === 0" class="empty-container">
          <div class="empty-icon">📚</div>
          <h3>暂无词库</h3>
          <p>请先创建词库后再进行关卡挑战</p>
          <button @click="$emit('create-library')" class="create-button">
            创建词库
          </button>
        </div>

        <div v-else class="libraries-list">
          <div class="search-container">
            <input
              v-model="searchQuery"
              @input="filterLibraries"
              type="text"
              placeholder="搜索词库..."
              class="search-input"
            />
          </div>

          <div class="libraries-grid">
            <div
              v-for="library in filteredLibraries"
              :key="library.id"
              class="library-card"
              :class="{ 'selected': selectedLibrary?.id === library.id }"
              @click="selectLibrary(library)"
            >
              <div class="library-header">
                <h3 class="library-name">{{ library.name }}</h3>
                <span class="difficulty-badge" :class="`difficulty-${library.difficulty_level}`">
                  {{ getDifficultyText(library.difficulty_level) }}
                </span>
              </div>
              
              <div class="library-description" v-if="library.description">
                {{ library.description }}
              </div>
              
              <div class="library-stats">
                <span class="stat-item">
                  <span class="stat-label">词组:</span>
                  <span class="stat-value">{{ library.groups_count || 0 }}</span>
                </span>
                <span class="stat-item">
                  <span class="stat-label">单词:</span>
                  <span class="stat-value">{{ library.words_count || 0 }}</span>
                </span>
              </div>

              <div class="library-tags" v-if="library.tags && library.tags.length > 0">
                <span
                  v-for="tag in library.tags.slice(0, 3)"
                  :key="tag"
                  class="tag"
                >
                  {{ tag }}
                </span>
                <span v-if="library.tags.length > 3" class="tag-more">
                  +{{ library.tags.length - 3 }}
                </span>
              </div>

              <div class="selection-indicator" v-if="selectedLibrary?.id === library.id">
                ✓
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer" v-if="!loading && !error && libraries.length > 0">
        <button @click="$emit('close')" class="btn btn-secondary">
          取消
        </button>
        <button 
          @click="confirmSelection" 
          :disabled="!selectedLibrary"
          class="btn btn-primary"
        >
          确认选择
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { vocabularyApi } from '../../utils/vocabularyApi.js'

const emit = defineEmits(['close', 'select', 'create-library'])

// 数据状态
const libraries = ref([])
const filteredLibraries = ref([])
const selectedLibrary = ref(null)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')

// 加载词库列表
const loadLibraries = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await vocabularyApi.getLibraries()
    console.log('词库API响应:', response)
    
    if (response.success) {
      // 处理不同的数据格式
      let librariesData = response.data
      if (librariesData && typeof librariesData === 'object') {
        // 如果data是对象，可能包含libraries字段
        if (librariesData.libraries && Array.isArray(librariesData.libraries)) {
          librariesData = librariesData.libraries
        } else if (Array.isArray(librariesData)) {
          // 如果data本身就是数组
          librariesData = librariesData
        } else {
          // 如果都不是，设为空数组
          librariesData = []
        }
      } else {
        librariesData = []
      }
      
      libraries.value = librariesData
      filteredLibraries.value = [...libraries.value]
    } else {
      throw new Error(response.message || '获取词库失败')
    }
  } catch (err) {
    console.error('加载词库失败:', err)
    error.value = err.message || '加载词库失败，请重试'
    // 设置空数组避免迭代错误
    libraries.value = []
    filteredLibraries.value = []
  } finally {
    loading.value = false
  }
}

// 筛选词库
const filterLibraries = () => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) {
    filteredLibraries.value = [...libraries.value]
  } else {
    filteredLibraries.value = libraries.value.filter(library => 
      library.name.toLowerCase().includes(query) ||
      (library.description && library.description.toLowerCase().includes(query)) ||
      (library.tags && library.tags.some(tag => tag.toLowerCase().includes(query)))
    )
  }
}

// 选择词库
const selectLibrary = (library) => {
  selectedLibrary.value = library
}

// 确认选择
const confirmSelection = () => {
  if (selectedLibrary.value) {
    emit('select', selectedLibrary.value)
  }
}

// 获取难度文本
const getDifficultyText = (level) => {
  const texts = ['', '初级', '中级', '中高级', '高级', '专家级']
  return texts[level] || '未知'
}

// 组件挂载时加载数据
onMounted(() => {
  loadLibraries()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  flex-shrink: 0;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  color: #666;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.loading-container,
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  text-align: center;
}

.loading-text {
  font-size: 16px;
  color: #666;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.error-container {
  background: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 20px;
}

.error-text {
  font-size: 16px;
  color: #dc2626;
  margin-bottom: 16px;
}

.retry-button {
  padding: 8px 16px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.retry-button:hover {
  background: #b91c1c;
}

.empty-container {
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-container h3 {
  margin: 0 0 8px 0;
  color: #333;
}

.empty-container p {
  margin: 0 0 20px 0;
  color: #666;
}

.create-button {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.create-button:hover {
  background: #0056b3;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.libraries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.library-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  background: white;
}

.library-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}

.library-card.selected {
  border-color: #007bff;
  background: #f8f9ff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.25);
}

.library-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.library-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 12px;
}

.difficulty-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.difficulty-1 { background: #e8f5e8; color: #2e7d32; }
.difficulty-2 { background: #fff3cd; color: #f57c00; }
.difficulty-3 { background: #ffeaa7; color: #e65100; }
.difficulty-4 { background: #ffcdd2; color: #c62828; }
.difficulty-5 { background: #f3e5f5; color: #7b1fa2; }

.library-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.library-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.stat-item {
  font-size: 13px;
}

.stat-label {
  color: #666;
}

.stat-value {
  color: #333;
  font-weight: 500;
}

.library-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.tag-more {
  background: #f5f5f5;
  color: #666;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
}

.selection-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  flex-shrink: 0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .libraries-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .library-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .library-name {
    margin-right: 0;
  }
}
</style>