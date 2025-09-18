<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ isEdit ? '编辑词组' : '创建词组' }}</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-group">
          <label for="name">词组名称 *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            placeholder="请输入词组名称"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="description">描述</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="请输入词组描述"
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

        <div class="form-group" v-if="isEdit">
          <label class="checkbox-label">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="form-checkbox"
            />
            启用词组
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
import { vocabularyApi } from '@/utils/vocabularyApi.js'

export default {
  name: 'GroupModal',
  props: {
    group: {
      type: Object,
      default: null
    },
    libraryId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const loading = ref(false)
    
    const form = reactive({
      name: '',
      description: '',
      difficulty_level: 1,
      sort_order: 0,
      is_active: true
    })

    const isEdit = computed(() => !!props.group)

    // 初始化表单
    const initForm = () => {
      if (props.group) {
        form.name = props.group.name
        form.description = props.group.description || ''
        form.difficulty_level = props.group.difficulty_level
        form.sort_order = props.group.sort_order
        form.is_active = props.group.is_active
      }
    }

    // 提交表单
    const handleSubmit = async () => {
      try {
        loading.value = true
        
        const data = {
          name: form.name,
          description: form.description,
          difficulty_level: parseInt(form.difficulty_level),
          sort_order: form.sort_order
        }

        if (isEdit.value) {
          data.is_active = form.is_active
        }

        let response
        if (isEdit.value) {
          response = await vocabularyApi.updateGroup(props.group.id, data)
        } else {
          response = await vocabularyApi.createGroup(props.libraryId, data)
        }

        if (response.success) {
          alert(isEdit.value ? '词组更新成功' : '词组创建成功')
          emit('saved', response.data)
        }
      } catch (error) {
        console.error('保存词组失败:', error)
        alert(error.response?.data?.message || '保存词组失败，请重试')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      initForm()
    })

    return {
      loading,
      form,
      isEdit,
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
  z-index: 1200;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
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
}
</style>