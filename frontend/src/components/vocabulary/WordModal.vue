<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ isEdit ? '编辑单词' : '添加单词' }}</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-row">
          <div class="form-group">
            <label for="word">单词 *</label>
            <input
              id="word"
              v-model="form.word"
              type="text"
              required
              placeholder="请输入单词"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="part_of_speech">词性</label>
            <select id="part_of_speech" v-model="form.part_of_speech" class="form-select">
              <option value="">请选择</option>
              <option value="n.">名词</option>
              <option value="v.">动词</option>
              <option value="adj.">形容词</option>
              <option value="adv.">副词</option>
              <option value="prep.">介词</option>
              <option value="conj.">连词</option>
              <option value="pron.">代词</option>
              <option value="art.">冠词</option>
              <option value="num.">数词</option>
              <option value="int.">感叹词</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label for="translation">翻译 *</label>
          <input
            id="translation"
            v-model="form.translation"
            type="text"
            required
            placeholder="请输入中文翻译"
            class="form-input"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="pronunciation">发音</label>
            <input
              id="pronunciation"
              v-model="form.pronunciation"
              type="text"
              placeholder="如：hello"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="phonetic">音标</label>
            <input
              id="phonetic"
              v-model="form.phonetic"
              type="text"
              placeholder="如：/həˈloʊ/"
              class="form-input"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="example_sentence">例句</label>
          <textarea
            id="example_sentence"
            v-model="form.example_sentence"
            placeholder="请输入英文例句"
            rows="2"
            class="form-textarea"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="example_translation">例句翻译</label>
          <textarea
            id="example_translation"
            v-model="form.example_translation"
            placeholder="请输入例句的中文翻译"
            rows="2"
            class="form-textarea"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="notes">备注</label>
          <textarea
            id="notes"
            v-model="form.notes"
            placeholder="请输入备注信息"
            rows="2"
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
              placeholder="输入标签后按回车或逗号添加"
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
            启用单词
          </label>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            取消
          </button>
          <button type="submit" :disabled="loading" class="btn btn-primary">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? '保存中...' : (isEdit ? '更新' : '添加') }}
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
  name: 'WordModal',
  props: {
    word: {
      type: Object,
      default: null
    },
    groupId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const loading = ref(false)
    const tagInput = ref('')
    
    const form = reactive({
      word: '',
      translation: '',
      pronunciation: '',
      phonetic: '',
      part_of_speech: '',
      difficulty_level: 1,
      example_sentence: '',
      example_translation: '',
      notes: '',
      sort_order: 0,
      tags: [],
      is_active: true
    })

    const commonTags = ['重点', '高频', '易错', '基础', '进阶', '口语', '写作', '阅读', '听力']

    const isEdit = computed(() => !!props.word)

    // 初始化表单
    const initForm = () => {
      if (props.word) {
        form.word = props.word.word
        form.translation = props.word.translation
        form.pronunciation = props.word.pronunciation || ''
        form.phonetic = props.word.phonetic || ''
        form.part_of_speech = props.word.part_of_speech || ''
        form.difficulty_level = props.word.difficulty_level
        form.example_sentence = props.word.example_sentence || ''
        form.example_translation = props.word.example_translation || ''
        form.notes = props.word.notes || ''
        form.sort_order = props.word.sort_order
        form.tags = [...(props.word.tags || [])]
        form.is_active = props.word.is_active
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
          word: form.word,
          translation: form.translation,
          pronunciation: form.pronunciation,
          phonetic: form.phonetic,
          part_of_speech: form.part_of_speech,
          difficulty_level: parseInt(form.difficulty_level),
          example_sentence: form.example_sentence,
          example_translation: form.example_translation,
          notes: form.notes,
          sort_order: form.sort_order,
          tags: form.tags
        }

        if (isEdit.value) {
          data.is_active = form.is_active
        }

        let response
        if (isEdit.value) {
          response = await vocabularyApi.updateWord(props.word.id, data)
        } else {
          response = await vocabularyApi.createWord(props.groupId, data)
        }

        if (response.success) {
          alert(isEdit.value ? '单词更新成功' : '单词添加成功')
          emit('saved', response.data)
        }
      } catch (error) {
        console.error('保存单词失败:', error)
        alert(error.response?.data?.message || '保存单词失败，请重试')
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
  z-index: 1300;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 700px;
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
  min-height: 60px;
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