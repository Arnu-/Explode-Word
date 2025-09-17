<template>
  <div class="library-detail-panel">
    <div class="panel-overlay" @click="$emit('close')"></div>
    <div class="panel-content">
      <div class="panel-header">
        <div class="library-info">
          <h2>{{ library.name }}</h2>
          <div class="library-meta">
            <span class="meta-item">
              <strong>词组数:</strong> {{ library.groups_count }}
            </span>
            <span class="meta-item">
              <strong>单词数:</strong> {{ library.total_words_count }}
            </span>
            <span class="meta-item">
              <strong>难度:</strong> {{ getDifficultyText(library.difficulty_level) }}
            </span>
          </div>
        </div>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <div class="panel-body">
        <!-- 词库描述 -->
        <div class="section" v-if="library.description">
          <h3>描述</h3>
          <p>{{ library.description }}</p>
        </div>

        <!-- 标签 -->
        <div class="section" v-if="library.tags.length > 0">
          <h3>标签</h3>
          <div class="tags">
            <span v-for="tag in library.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>

        <!-- 词组管理 -->
        <div class="section">
          <div class="section-header">
            <h3>词组管理</h3>
            <button @click="showCreateGroupModal = true" class="btn btn-primary btn-sm">
              <span class="icon">+</span>
              添加词组
            </button>
          </div>

          <!-- 词组搜索 -->
          <div class="search-box">
            <input 
              v-model="groupSearchQuery" 
              @input="debounceGroupSearch"
              placeholder="搜索词组..."
              class="search-input"
            />
          </div>

          <!-- 词组列表 -->
          <div class="groups-list" v-if="groups.length > 0">
            <div 
              v-for="group in groups" 
              :key="group.id" 
              class="group-item"
              @click="selectGroup(group)"
              :class="{ active: selectedGroup?.id === group.id }"
            >
              <div class="group-info">
                <h4>{{ group.name }}</h4>
                <p v-if="group.description">{{ group.description }}</p>
                <div class="group-stats">
                  <span>{{ group.words_count }} 个单词</span>
                  <span>难度: {{ getDifficultyText(group.difficulty_level) }}</span>
                  <span :class="['status', group.is_active ? 'active' : 'inactive']">
                    {{ group.is_active ? '启用' : '禁用' }}
                  </span>
                </div>
              </div>
              <div class="group-actions">
                <button @click.stop="editGroup(group)" class="btn-icon" title="编辑">
                  ✏️
                </button>
                <button @click.stop="deleteGroup(group)" class="btn-icon" title="删除">
                  🗑️
                </button>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else-if="!groupsLoading" class="empty-state">
            <p>暂无词组，点击"添加词组"开始创建</p>
          </div>

          <!-- 加载状态 -->
          <div v-if="groupsLoading" class="loading">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <!-- 词组分页 -->
          <div class="pagination" v-if="groupPagination.pages > 1">
            <button 
              @click="changeGroupPage(groupPagination.page - 1)"
              :disabled="!groupPagination.has_prev"
              class="btn btn-secondary btn-sm"
            >
              上一页
            </button>
            <span class="page-info">
              第 {{ groupPagination.page }} 页，共 {{ groupPagination.pages }} 页
            </span>
            <button 
              @click="changeGroupPage(groupPagination.page + 1)"
              :disabled="!groupPagination.has_next"
              class="btn btn-secondary btn-sm"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 词组详情面板 -->
    <GroupDetailPanel 
      v-if="selectedGroup"
      :group="selectedGroup"
      @close="selectedGroup = null"
      @updated="handleGroupUpdated"
    />

    <!-- 创建/编辑词组模态框 -->
    <GroupModal
      v-if="showCreateGroupModal || editingGroup"
      :group="editingGroup"
      :library-id="library.id"
      @close="closeGroupModal"
      @saved="handleGroupSaved"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { vocabularyApi } from '../../utils/vocabularyApi.js'
import GroupDetailPanel from './GroupDetailPanel.vue'
import GroupModal from './GroupModal.vue'

export default {
  name: 'LibraryDetailPanel',
  components: {
    GroupDetailPanel,
    GroupModal
  },
  props: {
    library: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'updated'],
  setup(props, { emit }) {
    const groups = ref([])
    const selectedGroup = ref(null)
    const groupsLoading = ref(false)
    const groupSearchQuery = ref('')
    const showCreateGroupModal = ref(false)
    const editingGroup = ref(null)
    
    const groupPagination = reactive({
      page: 1,
      per_page: 10,
      total: 0,
      pages: 0,
      has_prev: false,
      has_next: false
    })

    // 加载词组列表
    const loadGroups = async () => {
      try {
        groupsLoading.value = true
        const params = {
          page: groupPagination.page,
          per_page: groupPagination.per_page
        }
        
        if (groupSearchQuery.value.trim()) {
          params.search = groupSearchQuery.value.trim()
        }
        
        const response = await vocabularyApi.getGroups(props.library.id, params)
        if (response.success) {
          groups.value = response.data.groups
          Object.assign(groupPagination, response.data.pagination)
        }
      } catch (error) {
        console.error('加载词组失败:', error)
        alert('加载词组失败，请重试')
      } finally {
        groupsLoading.value = false
      }
    }

    // 防抖搜索
    let groupSearchTimeout = null
    const debounceGroupSearch = () => {
      clearTimeout(groupSearchTimeout)
      groupSearchTimeout = setTimeout(() => {
        groupPagination.page = 1
        loadGroups()
      }, 500)
    }

    // 选择词组
    const selectGroup = (group) => {
      selectedGroup.value = group
    }

    // 编辑词组
    const editGroup = (group) => {
      editingGroup.value = group
    }

    // 删除词组
    const deleteGroup = async (group) => {
      if (!confirm(`确定要删除词组"${group.name}"吗？此操作不可恢复。`)) {
        return
      }
      
      try {
        const response = await vocabularyApi.deleteGroup(group.id)
        if (response.success) {
          alert('词组删除成功')
          if (selectedGroup.value?.id === group.id) {
            selectedGroup.value = null
          }
          loadGroups()
          // 更新词库信息
          emit('updated', { ...props.library, groups_count: props.library.groups_count - 1 })
        }
      } catch (error) {
        console.error('删除词组失败:', error)
        alert(error.response?.data?.message || '删除词组失败，请重试')
      }
    }

    // 关闭词组模态框
    const closeGroupModal = () => {
      showCreateGroupModal.value = false
      editingGroup.value = null
    }

    // 处理词组保存
    const handleGroupSaved = (group) => {
      closeGroupModal()
      loadGroups()
      if (selectedGroup.value?.id === group.id) {
        selectedGroup.value = group
      }
      // 更新词库信息
      if (!editingGroup.value) {
        emit('updated', { ...props.library, groups_count: props.library.groups_count + 1 })
      }
    }

    // 处理词组更新
    const handleGroupUpdated = (group) => {
      const index = groups.value.findIndex(g => g.id === group.id)
      if (index !== -1) {
        groups.value[index] = group
      }
      selectedGroup.value = group
    }

    // 切换词组页面
    const changeGroupPage = (page) => {
      groupPagination.page = page
      loadGroups()
    }

    // 获取难度文本
    const getDifficultyText = (level) => {
      const texts = ['', '初级', '中级', '中高级', '高级', '专家级']
      return texts[level] || '未知'
    }

    // 监听词库变化
    watch(() => props.library.id, () => {
      groups.value = []
      selectedGroup.value = null
      groupPagination.page = 1
      loadGroups()
    })

    onMounted(() => {
      loadGroups()
    })

    return {
      groups,
      selectedGroup,
      groupsLoading,
      groupSearchQuery,
      showCreateGroupModal,
      editingGroup,
      groupPagination,
      loadGroups,
      debounceGroupSearch,
      selectGroup,
      editGroup,
      deleteGroup,
      closeGroupModal,
      handleGroupSaved,
      handleGroupUpdated,
      changeGroupPage,
      getDifficultyText
    }
  }
}
</script>

<style scoped>
.library-detail-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
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
  width: 600px;
  max-width: 90vw;
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

.library-info h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
}

.library-meta {
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

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
}

.search-box {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.groups-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.group-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.group-item:hover {
  border-color: #007bff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.group-item.active {
  border-color: #007bff;
  background: #f8f9ff;
}

.group-info {
  flex: 1;
}

.group-info h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.group-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.group-stats {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.group-actions {
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
  padding: 2px 8px;
  border-radius: 10px;
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
  
  .library-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .group-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .group-actions {
    align-self: flex-end;
  }
  
  .group-stats {
    flex-direction: column;
    gap: 5px;
  }
}
</style>