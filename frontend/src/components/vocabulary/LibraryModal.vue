<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ isEdit ? '编辑词库' : '创建词库' }}</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-group">
          <label for="name">词库名称 *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="请输入词库名称"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="description">描述</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="请输入词库描述"
            rows="3"
            class="form-textarea"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="difficulty_level">难度等级</label>
            <select id="difficulty_level" v-model="form.difficulty_level" class="form-select">
              <option value="1">初级</option>
              <option value="2">中级</option>
              <option value="3">中高级</option>
              <option value="4">高级</option>
              <option value="5">专家级</option>
            </select>
          </div>

          <div class="form-group">
            <label for="sort_order">排序</label>
            <input
              id="sort_order"
              v-model.number="form.sort_order"
              type="number"
              min="0"
              placeholder="0"
              class="form-input"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="tags">标签</label>
          <div class="tags-input-container">
            <div class="tags-display" v-if="form.tags.length > 0">
              <span 
                v-for="(tag, index) in form.tags" 
                :key="index" 
                class="tag"
              >
                {{ tag }}
                <button 
                  type="button" 
                  @click="removeTag(index)" 
                  class="tag-remove"
                >
                  ×
                </button>
              </span>
            </div>
            <input
              id="tags"
              v-model="tagInput"
              @keydown.enter.prevent="addTag"
              @keydown.comma.prevent="addTag"
              type="text"
              placeholder="输入标签后按回车或逗号添加（如：人教版、部编版）"
              class="form-input"
            />
          </div>
          <div class="form-help">
            常用标签：
            <button 
              v-for="commonTag in commonTags" 
              :key="commonTag"
              type="button"
              @click="addCommonTag(commonTag)"
              class="common-tag-btn"
            >
              {{ commonTag }}
            </button>
          </div>
        </div>

        <div class="form-group" v-if="isEdit">
          <label class="checkbox-label">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="form-checkbox"
            />
            启用词库
          </label>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            取消
          </button>
          <button type="submit" :disabled="loading" class="btn btn-primary">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? '保存中...' : (isEdit ? '更新' : '创建') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { vocabularyApi } from '../../utils/vocabularyApi.js'

export default {
  name: 'LibraryModal',
  props: {
    library: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const loading = ref(false)
    const tagInput = ref('')
    
    const form = reactive({
      name: '',
      description: '',
      difficulty_level: 1,
      sort_order: 0,
      tags: [],
      is_active: true
    })

    const commonTags = ['人教版', '部编版', '苏教版', '北师大版', '外研版', '牛津版', '新概念', '四级', '六级', '托福', '雅思']

    const isEdit = computed(() => !!props.library)

    // 初始化表单
    const initForm = () => {
      if (props.library) {
        form.name = props.library.name
        form.description = props.library.description || ''
        form.difficulty_level = props.library.difficulty_level
        form.sort_order = props.library.sort_order
        form.tags = [...(props.library.tags || [])]
        form.is_active = props.library.is_active
      }
    }

    // 添加标签
    const addTag = () => {
      const tag = tagInput.value.trim()
      if (tag && !form.tags.includes(tag)) {
        form.tags.push(tag)
        tagInput.value = ''
      }
    }

    // 添加常用标签
    const addCommonTag = (tag) => {
      if (!form.tags.includes(tag)) {
        form.tags.push(tag)
      }
    }

    // 移除标签
    const removeTag = (index) => {
      form.tags.splice(index, 1)
    }

    // 提交表单
    const handleSubmit = async () => {
      try {
        loading.value = true
        
        const data = {
          name: form.name,
          description: form.description,
          difficulty_level: parseInt(form.difficulty_level),
          sort_order: form.sort_order,
          tags: form.tags
        }

        if (isEdit.value) {
          data.is_active = form.is_active
        }

        let response
        if (isEdit.value) {
          response = await vocabularyApi.updateLibrary(props.library.id, data)
        } else {
          response = await vocabularyApi.createLibrary(data)
        }

        if (response.success) {
          alert(isEdit.value ? '词库更新成功' : '词库创建成功')
          emit('saved', response.data)
        }
      } catch (error) {
        console.error('保存词库失败:', error)
        alert(error.response?.data?.message || '保存词库失败，请重试')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      initForm()
    })

    return {
      loading,
      tagInput,
      form,
      commonTags,
      isEdit,
      addTag,
      addCommonTag,
      removeTag,
      handleSubmit
    }
  }
}
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
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
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.tags-input-container {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px;
  min-height: 40px;
}

.tags-display {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tag-remove {
  background: none;
  border: none;
  color: #1976d2;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.tag-remove:hover {
  background: rgba(25, 118, 210, 0.1);
}

.tags-input-container .form-input {
  border: none;
  padding: 4px 0;
  box-shadow: none;
}

.tags-input-container .form-input:focus {
  box-shadow: none;
}

.form-help {
  margin-top: 8px;
  font-size: 12px;
  color: #666;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.common-tag-btn {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #495057;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.common-tag-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-checkbox {
  width: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
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
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .form-help {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>