<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>批量导入单词</h2>
        <button @click="$emit('close')" class="close-btn">×</button>
      </div>

      <div class="modal-body">
        <div class="import-tabs">
          <button 
            @click="activeTab = 'manual'"
            :class="['tab-btn', { active: activeTab === 'manual' }]"
          >
            手动输入
          </button>
          <button 
            @click="activeTab = 'file'"
            :class="['tab-btn', { active: activeTab === 'file' }]"
          >
            文件导入
          </button>
        </div>

        <!-- 手动输入 -->
        <div v-if="activeTab === 'manual'" class="tab-content">
          <div class="form-group">
            <label>批量输入单词</label>
            <textarea
              v-model="manualInput"
              placeholder="请按以下格式输入，每行一个单词：&#10;单词,翻译,词性,发音,音标,例句,例句翻译,备注,难度等级,标签1,标签2,...&#10;&#10;示例：&#10;hello,你好,int.,həˈloʊ,/həˈloʊ/,Hello world,你好世界,常用问候语,1,基础,口语&#10;suppose,假设，认为,v.,səˈpəʊz,/səˈpəʊz/,I suppose you're right.,我认为你是对的,,3,Unit 1,词汇"
              rows="12"
              class="form-textarea"
            ></textarea>
          </div>
          
          <div class="format-help">
            <h4>格式说明：</h4>
            <ul>
              <li><strong>必填字段：</strong>单词、翻译</li>
              <li><strong>字段顺序：</strong>单词,翻译,词性,发音,音标,例句,例句翻译,备注,难度等级(1-5),标签1,标签2,...</li>
              <li><strong>分隔符：</strong>使用英文逗号(,)分隔各字段</li>
              <li><strong>标签：</strong>可以有多个标签，每个标签作为独立字段，如：Unit 1,词汇,重点</li>
              <li><strong>空字段：</strong>可以留空，但逗号不能省略</li>
            </ul>
          </div>
        </div>

        <!-- 文件导入 -->
        <div v-if="activeTab === 'file'" class="tab-content">
          <div class="form-group">
            <label>选择文件</label>
            <div class="file-upload-area" @drop="handleFileDrop" @dragover.prevent @dragenter.prevent>
              <input
                ref="fileInput"
                type="file"
                accept=".csv,.txt"
                @change="handleFileSelect"
                class="file-input"
              />
              <div class="upload-content">
                <div class="upload-icon">📁</div>
                <p>点击选择文件或拖拽文件到此处</p>
                <p class="upload-hint">支持 CSV 和 TXT 文件</p>
              </div>
            </div>
          </div>

          <div v-if="selectedFile" class="selected-file">
            <div class="file-info">
              <span class="file-name">{{ selectedFile.name }}</span>
              <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
            </div>
            <button @click="removeFile" class="remove-file-btn">×</button>
          </div>

          <div class="format-help">
            <h4>文件格式要求：</h4>
            <ul>
              <li>CSV文件：使用逗号分隔，第一行可以是标题行</li>
              <li>TXT文件：每行一个单词，格式同手动输入</li>
              <li>编码：建议使用UTF-8编码</li>
            </ul>
          </div>
        </div>

        <!-- 预览区域 -->
        <div v-if="previewWords.length > 0" class="preview-section">
          <h4>预览 (前{{ Math.min(previewWords.length, 10) }}条)</h4>
          <div class="preview-table-container">
            <table class="preview-table">
              <thead>
                <tr>
                  <th>单词</th>
                  <th>翻译</th>
                  <th>词性</th>
                  <th>发音</th>
                  <th>音标</th>
                  <th>例句</th>
                  <th>例句翻译</th>
                  <th>备注</th>
                  <th>难度</th>
                  <th>标签</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(word, index) in previewWords.slice(0, 10)" :key="index" class="preview-row">
                  <td class="word-cell">
                    <strong>{{ word.word }}</strong>
                  </td>
                  <td class="translation-cell">{{ word.translation }}</td>
                  <td class="pos-cell">
                    <span v-if="word.part_of_speech" class="part-of-speech">{{ word.part_of_speech }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="pronunciation-cell">
                    <span v-if="word.pronunciation" class="example-text">{{ word.pronunciation }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="phonetic-cell">
                    <span v-if="word.phonetic" class="example-text">{{ word.phonetic }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="example-cell">
                    <span v-if="word.example_sentence" class="example-text">{{ word.example_sentence }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="example-trans-cell">
                    <span v-if="word.example_translation" class="example-trans-text">{{ word.example_translation }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="notes-cell">
                    <span v-if="word.notes">{{ word.notes }}</span>
                    <span v-else class="empty-field">-</span>
                  </td>
                  <td class="difficulty-cell">
                    <span class="difficulty-badge" :class="`difficulty-${word.difficulty_level}`">
                      {{ word.difficulty_level }}
                    </span>
                  </td>
                  <td class="tags-cell">
                    <div v-if="word.tags && word.tags.length > 0" class="tags-container">
                      <span v-for="tag in word.tags" :key="tag" class="tag">{{ tag }}</span>
                    </div>
                    <span v-else class="empty-field">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="preview-summary">
            共 {{ previewWords.length }} 个单词待导入
            <span v-if="parseErrors.length > 0" class="error-count">
              ({{ parseErrors.length }} 个错误)
            </span>
          </p>
        </div>

        <!-- 错误信息 -->
        <div v-if="parseErrors.length > 0" class="error-section">
          <h4>解析错误</h4>
          <div class="error-list">
            <div v-for="error in parseErrors.slice(0, 10)" :key="error.line" class="error-item">
              第{{ error.line }}行: {{ error.message }}
            </div>
          </div>
          <p v-if="parseErrors.length > 10" class="error-more">
            还有 {{ parseErrors.length - 10 }} 个错误...
          </p>
        </div>

        <div class="modal-footer">
          <button @click="parseInput" :disabled="!canParse" class="btn btn-secondary">
            解析预览
          </button>
          <button @click="$emit('close')" class="btn btn-secondary">
            取消
          </button>
          <button 
            @click="handleImport" 
            :disabled="loading || previewWords.length === 0" 
            class="btn btn-primary"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? '导入中...' : `导入 ${previewWords.length} 个单词` }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { vocabularyApi } from '@/utils/vocabularyApi.js'

export default {
  name: 'BatchImportModal',
  props: {
    groupId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'imported'],
  setup(props, { emit }) {
    const loading = ref(false)
    const activeTab = ref('manual')
    const manualInput = ref('')
    const selectedFile = ref(null)
    const fileInput = ref(null)
    const previewWords = ref([])
    const parseErrors = ref([])

    const canParse = computed(() => {
      return (activeTab.value === 'manual' && manualInput.value.trim()) ||
             (activeTab.value === 'file' && selectedFile.value)
    })

    // 处理文件选择
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        previewWords.value = []
        parseErrors.value = []
      }
    }

    // 处理文件拖拽
    const handleFileDrop = (event) => {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && (file.type === 'text/csv' || file.type === 'text/plain' || file.name.endsWith('.csv') || file.name.endsWith('.txt'))) {
        selectedFile.value = file
        previewWords.value = []
        parseErrors.value = []
      }
    }

    // 移除文件
    const removeFile = () => {
      selectedFile.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
      previewWords.value = []
      parseErrors.value = []
    }

    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // 解析单词数据
    const parseWordLine = (line, lineNumber) => {
      const parts = line.split(',').map(part => part.trim())
      
      if (parts.length < 2) {
        throw new Error('至少需要单词和翻译两个字段')
      }

      // 处理特殊的数据格式：翻译和词性可能合并在一起
      let correctedParts = [...parts]
      
      // 检查第二个字段是否包含词性（以中文逗号+词性标记结尾）
      if (parts.length >= 2 && parts[1].match(/，[a-zA-Z]+\.?$/)) {
        const translationAndPos = parts[1]
        const lastCommaIndex = translationAndPos.lastIndexOf('，')
        if (lastCommaIndex > 0) {
          const translation = translationAndPos.substring(0, lastCommaIndex)
          const partOfSpeech = translationAndPos.substring(lastCommaIndex + 1)
          
          // 重新构建parts数组
          correctedParts = [
            parts[0],           // 单词
            translation,        // 翻译
            partOfSpeech,       // 词性
            ...parts.slice(2)   // 其余字段
          ]
        }
      }
      
      // 处理例句翻译字段可能包含额外内容的情况
      if (correctedParts.length >= 7 && correctedParts[6].includes('，，')) {
        const exampleTransParts = correctedParts[6].split('，，')
        correctedParts[6] = exampleTransParts[0] // 例句翻译
        
        // 如果有额外内容，需要重新分配后续字段
        if (exampleTransParts.length > 1) {
          const remaining = exampleTransParts[1]
          const remainingParts = remaining.split(',').map(p => p.trim()).filter(p => p)
          
          // 重新构建数组，插入备注字段和剩余字段
          correctedParts = [
            ...correctedParts.slice(0, 7), // 前7个字段（单词到例句翻译）
            '', // 备注字段（空）
            ...remainingParts, // 剩余字段（难度、标签等）
            ...correctedParts.slice(7) // 原来的后续字段
          ]
        }
      }

      // 验证必填字段
      const word = {
        word: correctedParts[0],
        translation: correctedParts[1],
        part_of_speech: correctedParts[2] || '',
        pronunciation: correctedParts[3] || '',
        phonetic: correctedParts[4] || '',
        example_sentence: correctedParts[5] || '',
        example_translation: correctedParts[6] || '',
        notes: correctedParts[7] || '',
        difficulty_level: parseInt(correctedParts[8]) || 1,
        tags: correctedParts.slice(9).filter(tag => tag.trim()).map(tag => tag.trim())
      }

      // 验证必填字段
      if (!word.word) {
        throw new Error('单词不能为空')
      }
      if (!word.translation) {
        throw new Error('翻译不能为空')
      }

      // 验证难度等级
      if (word.difficulty_level < 1 || word.difficulty_level > 5) {
        word.difficulty_level = 1
      }

      return word
    }

    // 解析输入内容
    const parseInput = async () => {
      previewWords.value = []
      parseErrors.value = []

      try {
        let content = ''
        
        if (activeTab.value === 'manual') {
          content = manualInput.value.trim()
        } else if (activeTab.value === 'file' && selectedFile.value) {
          content = await readFileContent(selectedFile.value)
        }

        if (!content) {
          return
        }

        const lines = content.split('\n').filter(line => line.trim())
        const words = []
        const errors = []

        lines.forEach((line, index) => {
          const lineNumber = index + 1
          try {
            // 跳过可能的标题行
            if (lineNumber === 1 && (line.includes('单词') || line.includes('word'))) {
              return
            }
            
            const word = parseWordLine(line, lineNumber)
            words.push(word)
          } catch (error) {
            errors.push({
              line: lineNumber,
              message: error.message
            })
          }
        })

        previewWords.value = words
        parseErrors.value = errors
      } catch (error) {
        console.error('解析失败:', error)
        alert('解析失败: ' + error.message)
      }
    }

    // 读取文件内容
    const readFileContent = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = (e) => reject(e)
        reader.readAsText(file, 'UTF-8')
      })
    }

    // 执行导入
    const handleImport = async () => {
      if (previewWords.value.length === 0) {
        alert('没有可导入的单词')
        return
      }

      try {
        loading.value = true
        
        const response = await vocabularyApi.batchImportWords(props.groupId, previewWords.value)

        if (response.success) {
          emit('imported', response.data)
        }
      } catch (error) {
        console.error('批量导入失败:', error)
        alert(error.response?.data?.message || '批量导入失败，请重试')
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      activeTab,
      manualInput,
      selectedFile,
      fileInput,
      previewWords,
      parseErrors,
      canParse,
      handleFileSelect,
      handleFileDrop,
      removeFile,
      formatFileSize,
      parseInput,
      handleImport
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
  z-index: 1400;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
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

.import-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.tab-btn {
  background: none;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.tab-btn.active {
  color: #007bff;
  border-bottom-color: #007bff;
}

.tab-btn:hover {
  color: #007bff;
}

.tab-content {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: monospace;
  resize: vertical;
  min-height: 200px;
}

.form-textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.file-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.file-upload-area:hover {
  border-color: #007bff;
  background: #f8f9ff;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-content {
  pointer-events: none;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.upload-hint {
  font-size: 12px;
  color: #666;
  margin: 5px 0 0 0;
}

.selected-file {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 15px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-name {
  font-weight: 500;
  color: #333;
}

.file-size {
  font-size: 12px;
  color: #666;
}

.remove-file-btn {
  background: #dc3545;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.format-help {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.format-help h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 14px;
}

.format-help ul {
  margin: 0;
  padding-left: 20px;
}

.format-help li {
  margin-bottom: 5px;
  font-size: 13px;
  color: #666;
}

.preview-section {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.preview-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.preview-table-container {
  overflow-x: auto;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
}

.preview-table th {
  background: #f8f9fa;
  color: #495057;
  font-weight: 600;
  padding: 12px 8px;
  text-align: left;
  border-bottom: 2px solid #e0e0e0;
  white-space: nowrap;
  font-size: 12px;
}

.preview-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: top;
  max-width: 150px;
  word-wrap: break-word;
}

.preview-row:hover {
  background: #f8f9ff;
}

.word-cell strong {
  color: #333;
  font-size: 14px;
}

.translation-cell {
  color: #666;
  font-weight: 500;
}

.part-of-speech {
  background: #e9ecef;
  color: #495057;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.empty-field {
  color: #ccc;
  font-style: italic;
}

.example-text, .example-trans-text {
  font-size: 12px;
  line-height: 1.4;
  display: block;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.example-text {
  color: #666;
}

.example-trans-text {
  color: #888;
}

.difficulty-badge {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 11px;
  font-weight: bold;
  color: white;
}

.difficulty-1 { background: #28a745; }
.difficulty-2 { background: #17a2b8; }
.difficulty-3 { background: #ffc107; color: #333; }
.difficulty-4 { background: #fd7e14; }
.difficulty-5 { background: #dc3545; }

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  max-width: 100px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 1px 4px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 500;
  white-space: nowrap;
}

/* 列宽控制 */
.preview-table th:nth-child(1), .preview-table td:nth-child(1) { width: 100px; } /* 单词 */
.preview-table th:nth-child(2), .preview-table td:nth-child(2) { width: 120px; } /* 翻译 */
.preview-table th:nth-child(3), .preview-table td:nth-child(3) { width: 60px; }  /* 词性 */
.preview-table th:nth-child(4), .preview-table td:nth-child(4) { width: 80px; }  /* 发音 */
.preview-table th:nth-child(5), .preview-table td:nth-child(5) { width: 80px; }  /* 音标 */
.preview-table th:nth-child(6), .preview-table td:nth-child(6) { width: 150px; } /* 例句 */
.preview-table th:nth-child(7), .preview-table td:nth-child(7) { width: 150px; } /* 例句翻译 */
.preview-table th:nth-child(8), .preview-table td:nth-child(8) { width: 100px; } /* 备注 */
.preview-table th:nth-child(9), .preview-table td:nth-child(9) { width: 50px; }  /* 难度 */
.preview-table th:nth-child(10), .preview-table td:nth-child(10) { width: 100px; } /* 标签 */

.preview-summary {
  margin: 15px 0 0 0;
  font-size: 14px;
  color: #333;
  text-align: center;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.error-count {
  color: #dc3545;
  font-weight: 500;
}

.error-section {
  border: 1px solid #dc3545;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
  background: #fff5f5;
}

.error-section h4 {
  margin: 0 0 10px 0;
  color: #dc3545;
  font-size: 14px;
}

.error-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.error-item {
  font-size: 13px;
  color: #dc3545;
  padding: 4px 8px;
  background: white;
  border-radius: 4px;
}

.error-more {
  margin: 10px 0 0 0;
  font-size: 12px;
  color: #666;
  text-align: center;
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

.btn-secondary:hover:not(:disabled) {
  background: #545b62;
}

.btn-secondary:disabled {
  background: #ccc;
  cursor: not-allowed;
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
  
  .import-tabs {
    flex-direction: column;
  }
  
  .tab-btn {
    text-align: left;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .file-upload-area {
    padding: 20px;
  }
  
  .upload-icon {
    font-size: 32px;
  }
}
</style>