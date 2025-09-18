<template>
  <div class="vocabulary-management">
    <div class="header">
      <div class="header-actions">
        <button @click="showCreateLibraryModal = true" class="btn btn-primary">
          <span class="icon">+</span>
          创建词库
        </button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filters">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @input="debounceSearch"
          placeholder="搜索词库名称或描述..."
          class="search-input"
        />
      </div>
      <div class="filter-tags">
        <input 
          v-model="tagFilter" 
          @input="debounceSearch"
          placeholder="按标签筛选（如：人教版,部编版）"
          class="tag-input"
        />
      </div>
      <div class="filter-status">
        <select v-model="statusFilter" @change="loadLibraries" class="status-select">
          <option value="">全部状态</option>
          <option value="true">启用</option>
          <option value="false">禁用</option>
        </select>
      </div>
    </div>

    <!-- 词库列表 -->
    <div class="libraries-grid" v-if="libraries.length > 0">
      <div 
        v-for="library in libraries" 
        :key="library.id" 
        class="library-card"
        @click="selectLibrary(library)"
        :class="{ active: selectedLibrary?.id === library.id }"
      >
        <div class="library-header">
          <h3>{{ library.name }}</h3>
          <div class="library-actions">
            <button @click.stop="editLibrary(library)" class="btn-icon" title="编辑">
              ✏️
            </button>
            <button @click.stop="deleteLibrary(library)" class="btn-icon" title="删除">
              🗑️
            </button>
          </div>
        </div>
        
        <p class="library-description">{{ library.description || '暂无描述' }}</p>
        
        <div class="library-tags" v-if="library.tags && library.tags.length > 0">
          <span v-for="tag in library.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
        
        <div class="library-stats">
          <div class="stat">
            <span class="stat-label">词组数:</span>
            <span class="stat-value">{{ library.groups_count }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">单词数:</span>
            <span class="stat-value">{{ library.total_words_count }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">难度:</span>
            <span class="stat-value">{{ getDifficultyText(library.difficulty_level) }}</span>
          </div>
        </div>
        
        <div class="library-status">
          <span :class="['status', library.is_active ? 'active' : 'inactive']">
            {{ library.is_active ? '启用' : '禁用' }}
          </span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading" class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>暂无词库</h3>
      <p>点击上方"创建词库"按钮开始创建您的第一个词库</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="pagination.pages > 1">
      <button 
        @click="changePage(pagination.page - 1)"
        :disabled="!pagination.has_prev"
        class="btn btn-secondary"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ pagination.page }} 页，共 {{ pagination.pages }} 页
      </span>
      <button 
        @click="changePage(pagination.page + 1)"
        :disabled="!pagination.has_next"
        class="btn btn-secondary"
      >
        下一页
      </button>
    </div>

    <!-- 词库详情面板 -->
    <LibraryDetailPanel 
      v-if="selectedLibrary"
      :library="selectedLibrary"
      @close="selectedLibrary = null"
      @updated="handleLibraryUpdated"
    />

    <!-- 创建/编辑词库模态框 -->
    <LibraryModal
      v-if="showCreateLibraryModal || editingLibrary"
      :library="editingLibrary"
      @close="closeLibraryModal"
      @saved="handleLibrarySaved"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { vocabularyApi } from '@/utils/vocabularyApi.js'
import LibraryDetailPanel from '@/components/vocabulary/LibraryDetailPanel.vue'
import LibraryModal from '@/components/vocabulary/LibraryModal.vue'

export default {
  name: 'VocabularyManagement',
  components: {
    LibraryDetailPanel,
    LibraryModal
  },
  setup() {
    const libraries = ref([])
    const selectedLibrary = ref(null)
    const loading = ref(false)
    const searchQuery = ref('')
    const tagFilter = ref('')
    const statusFilter = ref('')
    const showCreateLibraryModal = ref(false)
    const editingLibrary = ref(null)
    
    const pagination = reactive({
      page: 1,
      per_page: 12,
      total: 0,
      pages: 0,
      has_prev: false,
      has_next: false
    })

    // 加载词库列表
    const loadLibraries = async () => {
      try {
        loading.value = true
        const params = {
          page: pagination.page,
          per_page: pagination.per_page
        }
        
        if (searchQuery.value.trim()) {
          params.search = searchQuery.value.trim()
        }
        
        if (tagFilter.value.trim()) {
          params.tags = tagFilter.value.trim()
        }
        
        if (statusFilter.value !== '') {
          params.is_active = statusFilter.value === 'true'
        }
        
        const response = await vocabularyApi.getLibraries(params)
        if (response.success) {
          libraries.value = response.data.libraries
          Object.assign(pagination, response.data.pagination)
        }
      } catch (error) {
        console.error('加载词库失败:', error)
        alert('加载词库失败，请重试')
      } finally {
        loading.value = false
      }
    }

    // 防抖搜索
    let searchTimeout = null
    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        pagination.page = 1
        loadLibraries()
      }, 500)
    }

    // 选择词库
    const selectLibrary = (library) => {
      selectedLibrary.value = library
    }

    // 编辑词库
    const editLibrary = (library) => {
      editingLibrary.value = library
    }

    // 删除词库
    const deleteLibrary = async (library) => {
      if (!confirm(`确定要删除词库"${library.name}"吗？此操作不可恢复。`)) {
        return
      }
      
      try {
        const response = await vocabularyApi.deleteLibrary(library.id)
        if (response.success) {
          alert('词库删除成功')
          if (selectedLibrary.value?.id === library.id) {
            selectedLibrary.value = null
          }
          loadLibraries()
        }
      } catch (error) {
        console.error('删除词库失败:', error)
        alert(error.response?.data?.message || '删除词库失败，请重试')
      }
    }

    // 关闭词库模态框
    const closeLibraryModal = () => {
      showCreateLibraryModal.value = false
      editingLibrary.value = null
    }

    // 处理词库保存
    const handleLibrarySaved = (library) => {
      closeLibraryModal()
      loadLibraries()
      if (selectedLibrary.value?.id === library.id) {
        selectedLibrary.value = library
      }
    }

    // 处理词库更新
    const handleLibraryUpdated = (library) => {
      const index = libraries.value.findIndex(lib => lib.id === library.id)
      if (index !== -1) {
        libraries.value[index] = library
      }
      selectedLibrary.value = library
    }

    // 切换页面
    const changePage = (page) => {
      pagination.page = page
      loadLibraries()
    }

    // 获取难度文本
    const getDifficultyText = (level) => {
      const texts = ['', '初级', '中级', '中高级', '高级', '专家级']
      return texts[level] || '未知'
    }

    onMounted(() => {
      loadLibraries()
    })

    return {
      libraries,
      selectedLibrary,
      loading,
      searchQuery,
      tagFilter,
      statusFilter,
      showCreateLibraryModal,
      editingLibrary,
      pagination,
      loadLibraries,
      debounceSearch,
      selectLibrary,
      editLibrary,
      deleteLibrary,
      closeLibraryModal,
      handleLibrarySaved,
      handleLibraryUpdated,
      changePage,
      getDifficultyText
    }
  }
}
</script>

<style scoped>
.vocabulary-management {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  color: #333;
  font-size: 28px;
}

.header-actions .btn {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.search-input,
.tag-input,
.status-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  min-width: 200px;
}

.search-input:focus,
.tag-input:focus,
.status-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.libraries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.library-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.library-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.library-card.active {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.library-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.library-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.library-actions {
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

.library-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.4;
}

.library-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 15px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.library-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
}

.stat {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 2px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.library-status {
  text-align: right;
}

.status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
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
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
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
  gap: 20px;
  margin-top: 30px;
}

.page-info {
  color: #666;
  font-size: 14px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
  font-size: 16px;
}

@media (max-width: 768px) {
  .vocabulary-management {
    padding: 15px;
  }
  
  .header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .search-input,
  .tag-input,
  .status-select {
    min-width: auto;
  }
  
  .libraries-grid {
    grid-template-columns: 1fr;
  }
  
  .library-stats {
    flex-direction: column;
    gap: 10px;
  }
  
  .stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .stat-label,
  .stat-value {
    display: inline;
  }
}
</style>