<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人资料</h1>
      <p>管理您的账户信息和游戏设置</p>
    </div>

    <div class="profile-content">
      <!-- 基本信息卡片 -->
      <div class="profile-card">
        <h2>基本信息</h2>
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              id="username"
              v-model="profileForm.username"
              type="text"
              disabled
              class="form-input disabled"
            />
            <small class="form-help">用户名不可修改</small>
          </div>

          <div class="form-group">
            <label for="email">邮箱</label>
            <input
              id="email"
              v-model="profileForm.email"
              type="email"
              disabled
              class="form-input disabled"
            />
            <small class="form-help">邮箱不可修改</small>
          </div>

          <div class="form-group">
            <label for="nickname">昵称</label>
            <input
              id="nickname"
              v-model="profileForm.nickname"
              type="text"
              class="form-input"
              :disabled="profileLoading"
            />
          </div>

          <div class="form-group">
            <label for="avatar_url">头像链接</label>
            <input
              id="avatar_url"
              v-model="profileForm.avatar_url"
              type="url"
              class="form-input"
              placeholder="https://example.com/avatar.jpg"
              :disabled="profileLoading"
            />
          </div>

          <div v-if="profileError" class="error-message">
            {{ profileError }}
          </div>

          <div v-if="profileSuccess" class="success-message">
            {{ profileSuccess }}
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="profileLoading || !isProfileChanged"
          >
            <span v-if="profileLoading" class="loading-spinner"></span>
            {{ profileLoading ? '更新中...' : '更新资料' }}
          </button>
        </form>
      </div>

      <!-- 游戏统计卡片 -->
      <div class="profile-card">
        <h2>游戏统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">总游戏数</div>
            <div class="stat-value">{{ user?.total_games || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">胜利次数</div>
            <div class="stat-value">{{ user?.total_wins || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">胜率</div>
            <div class="stat-value">{{ user?.win_rate || 0 }}%</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">最高分</div>
            <div class="stat-value">{{ user?.best_score || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">平均分</div>
            <div class="stat-value">{{ user?.average_score || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">注册时间</div>
            <div class="stat-value">{{ formatDate(user?.created_at) }}</div>
          </div>
        </div>
      </div>

      <!-- 修改密码卡片 -->
      <div class="profile-card">
        <h2>修改密码</h2>
        <form @submit.prevent="changePassword" class="password-form">
          <div class="form-group">
            <label for="old_password">当前密码</label>
            <input
              id="old_password"
              v-model="passwordForm.old_password"
              type="password"
              class="form-input"
              required
              :disabled="passwordLoading"
            />
          </div>

          <div class="form-group">
            <label for="new_password">新密码</label>
            <input
              id="new_password"
              v-model="passwordForm.new_password"
              type="password"
              class="form-input"
              required
              :disabled="passwordLoading"
            />
          </div>

          <div class="form-group">
            <label for="confirm_password">确认新密码</label>
            <input
              id="confirm_password"
              v-model="passwordForm.confirm_password"
              type="password"
              class="form-input"
              required
              :disabled="passwordLoading"
            />
          </div>

          <div v-if="passwordError" class="error-message">
            {{ passwordError }}
          </div>

          <div v-if="passwordSuccess" class="success-message">
            {{ passwordSuccess }}
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="passwordLoading || !isPasswordFormValid"
          >
            <span v-if="passwordLoading" class="loading-spinner"></span>
            {{ passwordLoading ? '修改中...' : '修改密码' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuth } from '@/utils/auth.js'

export default {
  name: 'Profile',
  setup() {
    const { user, updateProfile, changePassword, getCurrentUser } = useAuth()

    // 资料表单
    const profileForm = ref({
      username: '',
      email: '',
      nickname: '',
      avatar_url: ''
    })

    // 密码表单
    const passwordForm = ref({
      old_password: '',
      new_password: '',
      confirm_password: ''
    })

    // 状态
    const profileLoading = ref(false)
    const profileError = ref('')
    const profileSuccess = ref('')
    const passwordLoading = ref(false)
    const passwordError = ref('')
    const passwordSuccess = ref('')

    // 原始用户数据（用于检测变化）
    const originalUserData = ref({})

    // 计算属性
    const isProfileChanged = computed(() => {
      return (
        profileForm.value.nickname !== originalUserData.value.nickname ||
        profileForm.value.avatar_url !== originalUserData.value.avatar_url
      )
    })

    const isPasswordFormValid = computed(() => {
      return (
        passwordForm.value.old_password &&
        passwordForm.value.new_password &&
        passwordForm.value.confirm_password &&
        passwordForm.value.new_password === passwordForm.value.confirm_password &&
        passwordForm.value.new_password.length >= 6
      )
    })

    // 方法
    const initializeForm = () => {
      if (user.value) {
        const userData = {
          username: user.value.username || '',
          email: user.value.email || '',
          nickname: user.value.nickname || '',
          avatar_url: user.value.avatar_url || ''
        }
        
        profileForm.value = { ...userData }
        originalUserData.value = { ...userData }
      }
    }

    const updateProfileHandler = async () => {
      profileLoading.value = true
      profileError.value = ''
      profileSuccess.value = ''

      try {
        const result = await updateProfile({
          nickname: profileForm.value.nickname,
          avatar_url: profileForm.value.avatar_url
        })

        if (result.success) {
          profileSuccess.value = '资料更新成功'
          originalUserData.value.nickname = profileForm.value.nickname
          originalUserData.value.avatar_url = profileForm.value.avatar_url
          
          // 3秒后清除成功消息
          setTimeout(() => {
            profileSuccess.value = ''
          }, 3000)
        } else {
          profileError.value = result.error
        }
      } catch (error) {
        profileError.value = error.message || '更新失败'
      } finally {
        profileLoading.value = false
      }
    }

    const changePasswordHandler = async () => {
      if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
        passwordError.value = '两次输入的新密码不一致'
        return
      }

      if (passwordForm.value.new_password.length < 6) {
        passwordError.value = '新密码长度至少6位'
        return
      }

      passwordLoading.value = true
      passwordError.value = ''
      passwordSuccess.value = ''

      try {
        const result = await changePassword({
          old_password: passwordForm.value.old_password,
          new_password: passwordForm.value.new_password
        })

        if (result.success) {
          passwordSuccess.value = '密码修改成功'
          // 清空表单
          passwordForm.value = {
            old_password: '',
            new_password: '',
            confirm_password: ''
          }
          
          // 3秒后清除成功消息
          setTimeout(() => {
            passwordSuccess.value = ''
          }, 3000)
        } else {
          passwordError.value = result.error
        }
      } catch (error) {
        passwordError.value = error.message || '密码修改失败'
      } finally {
        passwordLoading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      try {
        return new Date(dateString).toLocaleDateString('zh-CN')
      } catch {
        return '未知'
      }
    }

    // 监听用户数据变化
    watch(user, initializeForm, { immediate: true })

    // 生命周期
    onMounted(async () => {
      await getCurrentUser()
    })

    return {
      user: computed(() => user.value),
      profileForm,
      passwordForm,
      profileLoading,
      profileError,
      profileSuccess,
      passwordLoading,
      passwordError,
      passwordSuccess,
      isProfileChanged,
      isPasswordFormValid,
      updateProfile: updateProfileHandler,
      changePassword: changePasswordHandler,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
}

.profile-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.profile-header p {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.profile-card h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #e2e8f0;
}

.profile-form, .password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.form-input.disabled {
  background-color: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.form-help {
  font-size: 12px;
  color: #6b7280;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background-color: #f8fafc;
  border-radius: 8px;
}

.stat-label {
  font-size: 14px;
  color: #718096;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
}

.error-message {
  background-color: #fee;
  color: #c53030;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  border: 1px solid #fed7d7;
}

.success-message {
  background-color: #f0fff4;
  color: #38a169;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  border: 1px solid #9ae6b4;
}

.submit-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  align-self: flex-start;
}

.submit-button:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .profile-card {
    padding: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>