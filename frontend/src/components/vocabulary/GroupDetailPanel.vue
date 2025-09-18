<template>
  <div class="group-detail-panel">
    <div class="panel-overlay" @click="$emit('close')"></div>
    <div class="panel-content">
      <div class="panel-header">
        <div class="group-info">
          <h2>{{ group.name }}</h2>
          <div class="group-meta">
            <span class="meta-item">
              <strong>词库:</strong> {{ group.library_name }}
            </span>
            <span class="meta-item">
              <strong>单词数:</strong> {{ group.words_count }}
            </span>
            <span class="meta-item">
              <strong>难度:</strong> {{ getDifficultyText(group.difficulty_level) }}
            </span>
          </div>
        </div>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <div class="panel-body">
        <!-- 词组描述 -->
        <div class="section" v-if="group.description">
          <h3>描述</h3>
          <p>{{ group.description }}</p>
        </div>

        <!-- 单词管理 -->
        <div class="section">
          <div class="section-header">
            <h3>单词管理</h3>
            <div class="section-actions">
              <button @click="showBatchImportModal = true" class="btn btn-secondary btn-sm">
                <span class="icon">📥</span>
                批量导入
              </button>
              <button @click="showCreateWordModal = true" class="btn btn-primary btn-sm">
                <span class="icon">+</span>
                添加单词
              </button>
            </div>
          </div>

          <!-- 单词搜索和筛选 -->
          <div class="filters">
            <div class="search-box">
              <input 
                v-model="wordSearchQuery" 
                @input="debounceWordSearch"
                placeholder="搜索单词或翻译..."
                class="search-input"
              />
            </div>
            <div class="filter-tags">
              <input 
                v-model="wordTagFilter" 
                @input="debounceWordSearch"
                placeholder="按标签筛选"
                class="tag-input"
              />
            </div>
          </div>

          <!-- 单词列表 -->
          <div class="words-list" v-if="words.length > 0">
            <div 
              v-for="word in words" 
              :key="word.id" 
              class="word-item"
            >
              <div class="word-content">
                <div class="word-main">
                  <h4>{{ word.word }}</h4>
                  <div class="word-pronunciation" v-if="word.pronunciation || word.phonetic">
                    <span v-if="word.pronunciation">[{{ word.pronunciation }}]</span>
                    <span v-if="word.phonetic">{{ word.phonetic }}</span>
                  </div>
                </div>
                
                <div class="word-translation">
                  <span v-if="word.part_of_speech" class="part-of-speech">{{ word.part_of_speech }}</span>
                  {{ word.translation }}
                </div>
                
                <div class="word-example" v-if="word.example_sentence">
                  <div class="example-sentence">{{ word.example_sentence }}</div>
                  <div class="example-translation" v-if="word.example_translation">
                    {{ word.example_translation }}
                  </div>
                </div>
                
                <div class="word-tags" v-if="word.tags && word.tags.length > 0">
                  <span v-for="tag in word.tags" :key="tag" class="tag">{{ tag }}</span>
                </div>
                
                <div class="word-meta">
                  <span>难度: {{ getDifficultyText(word.difficulty_level) }}</span>
                  <span v-if="word.frequency > 0">使用: {{ word.frequency }}次</span>
                  <span :class="['status', word.is_active ? 'active' : 'inactive']">
                    {{ word.is_active ? '启用' : '禁用' }}
                  </span>
                </div>
              </div>
              
              <div class="word-actions">
                <button @click="editWord(word)" class="btn-icon" title="编辑">
                  ✏️
                </button>
                <button @click="deleteWord(word)" class="btn-icon" title="删除">
                  🗑️
                </button>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else-if="!wordsLoading" class="empty-state">
            <p>暂无单词，点击"添加单词"开始创建</p>
          </div>

          <!-- 加载状态 -->
          <div v-if="wordsLoading" class="loading">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <!-- 单词分页 -->
          <div class="pagination" v-if="wordPagination.pages > 1">
            <button 
              @click="changeWordPage(wordPagination.page - 1)"
              :disabled="!wordPagination.has_prev"
              class="btn btn-secondary btn-sm"
            >
              上一页
            </button>
            <span class="page-info">
              第 {{ wordPagination.page }} 页，共 {{ wordPagination.pages }} 页
            </span>
            <button 
              @click="changeWordPage(wordPagination.page + 1)"
              :disabled="!wordPagination.has_next"
              class="btn btn-secondary btn-sm"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑单词模态框 -->
    <WordModal
      v-if="showCreateWordModal || editingWord"
      :word="editingWord"
      :group-id="group.id"
      @close="closeWordModal"
      @saved="handleWordSaved"
    />

    <!-- 批量导入模态框 -->
    <BatchImportModal
      v-if="showBatchImportModal"
      :group-id="group.id"
      @close="showBatchImportModal = false"
      @imported="handleWordsImported"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { vocabularyApi } from '@/utils/vocabularyApi.js'
import WordModal from '@/components/vocabulary/WordModal.vue'
import BatchImportModal from '@/components/vocabulary/BatchImportModal.vue'

export default {
  name: 'GroupDetailPanel',
  components: {
    WordModal,
    BatchImportModal
  },
  props: {
    group: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'updated'],
  setup(props, { emit }) {
    const words = ref([])
    const wordsLoading = ref(false)
    const wordSearchQuery = ref('')
    const wordTagFilter = ref('')
    const showCreateWordModal = ref(false)
    const showBatchImportModal = ref(false)
    const editingWord = ref(null)
    
    const wordPagination = reactive({
      page: 1,
      per_page: 20,
      total: 0,
      pages: 0,
      has_prev: false,
      has_next: false
    })

    // 加载单词列表
    const loadWords = async () => {
      try {
        wordsLoading.value = true
        const params = {
          page: wordPagination.page,
          per_page: wordPagination.per_page
        }
        
        if (wordSearchQuery.value.trim()) {
          params.search = wordSearchQuery.value.trim()
        }
        
        if (wordTagFilter.value.trim()) {
          params.tags = wordTagFilter.value.trim()
        }
        
        const response = await vocabularyApi.getWords(props.group.id, params)
        if (response.success) {
          words.value = response.data.words
          Object.assign(wordPagination, response.data.pagination)
        }
      } catch (error) {
        console.error('加载单词失败:', error)
        alert('加载单词失败，请重试')
      } finally {
        wordsLoading.value = false
      }
    }

    // 防抖搜索
    let wordSearchTimeout = null
    const debounceWordSearch = () => {
      clearTimeout(wordSearchTimeout)
      wordSearchTimeout = setTimeout(() => {
        wordPagination.page = 1
        loadWords()
      }, 500)
    }

    // 编辑单词
    const editWord = (word) => {
      editingWord.value = word
    }

    // 删除单词
    const deleteWord = async (word) => {
      if (!confirm(`确定要删除单词"${word.word}"吗？此操作不可恢复。`)) {
        return
      }
      
      try {
        const response = await vocabularyApi.deleteWord(word.id)
        if (response.success) {
          alert('单词删除成功')
          loadWords()
          // 更新词组信息
          emit('updated', { ...props.group, words_count: props.group.words_count - 1 })
        }
      } catch (error) {
        console.error('删除单词失败:', error)
        alert(error.response?.data?.message || '删除单词失败，请重试')
      }
    }

    // 关闭单词模态框
    const closeWordModal = () => {
      showCreateWordModal.value = false
      editingWord.value = null
    }

    // 处理单词保存
    const handleWordSaved = (word) => {
      closeWordModal()
      loadWords()
      // 更新词组信息
      if (!editingWord.value) {
        emit('updated', { ...props.group, words_count: props.group.words_count + 1 })
      }
    }

    // 处理批量导入
    const handleWordsImported = (result) => {
      showBatchImportModal.value = false
      loadWords()
      // 更新词组信息
      emit('updated', { ...props.group, words_count: props.group.words_count + result.created_count })
      alert(`成功导入 ${result.created_count} 个单词`)
    }

    // 切换单词页面
    const changeWordPage = (page) => {
      wordPagination.page = page
      loadWords()
    }

    // 获取难度文本
    const getDifficultyText = (level) => {
      const texts = ['', '初级', '中级', '中高级', '高级', '专家级']
      return texts[level] || '未知'
    }

    // 监听词组变化
    watch(() => props.group.id, () => {
      words.value = []
      wordPagination.page = 1
      loadWords()
    })

    onMounted(() => {
      loadWords()
    })

    return {
      words,
      wordsLoading,
      wordSearchQuery,
      wordTagFilter,
      showCreateWordModal,
      showBatchImportModal,
      editingWord,
      wordPagination,
      loadWords,
      debounceWordSearch,
      editWord,
      deleteWord,
      closeWordModal,
      handleWordSaved,
      handleWordsImported,
      changeWordPage,
      getDifficultyText
    }
  }
}
</script>

<style scoped>
.group-detail-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1100;
  display: flex;
}

.panel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.panel-content {
  position: relative;
  width: 800px;
  max-width: 95vw;
  height: 100vh;
  background: white;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.group-info h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
}

.group-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.meta-item {
  font-size: 14px;
  color: #666;
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
  background: #e0e0e0;
  color: #333;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.section {
  margin-bottom: 30px;
}

.section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-actions {
  display: flex;
  gap: 10px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input,
.tag-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 200px;
}

.search-input:focus,
.tag-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.words-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.word-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.word-content {
  flex: 1;
}

.word-main {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 5px;
}

.word-main h4 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.word-pronunciation {
  font-size: 14px;
  color: #666;
  font-style: italic;
}

.word-translation {
  margin-bottom: 8px;
  color: #333;
  font-size: 15px;
}

.part-of-speech {
  background: #e9ecef;
  color: #495057;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  margin-right: 8px;
}

.word-example {
  margin-bottom: 10px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
  border-left: 3px solid #007bff;
}

.example-sentence {
  font-style: italic;
  color: #495057;
  margin-bottom: 4px;
}

.example-translation {
  font-size: 13px;
  color: #666;
}

.word-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 500;
}

.word-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.word-actions {
  display: flex;
  gap: 5px;
}

.btn-icon {
  background: none;
  border: none;
  padding: 5px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  opacity: 1;
  background: #f5f5f5;
}

.status {
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
}

.status.active {
  background: #e8f5e8;
  color: #2e7d32;
}

.status.inactive {
  background: #ffebee;
  color: #c62828;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.page-info {
  color: #666;
  font-size: 12px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-secondary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.icon {
  font-size: 14px;
}

@media (max-width: 768px) {
  .panel-content {
    width: 100vw;
    margin-left: 0;
  }
  
  .group-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .section-actions {
    justify-content: stretch;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .search-input,
  .tag-input {
    min-width: auto;
  }
  
  .word-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .word-actions {
    align-self: flex-end;
  }
  
  .word-meta {
    flex-direction: column;
    gap: 5px;
  }
  
  .word-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>