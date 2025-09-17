<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">{{ isLogin ? '登录' : '注册' }}</h1>
        <p class="login-subtitle">{{ isLogin ? '欢迎回到爆炸单词' : '加入爆炸单词' }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- 注册时显示昵称字段 -->
        <div v-if="!isLogin" class="form-group">
          <label for="nickname" class="form-label">昵称</label>
          <input
            id="nickname"
            v-model="form.nickname"
            type="text"
            class="form-input"
            placeholder="请输入昵称"
            :disabled="loading"
          />
        </div>

        <!-- 用户名字段 -->
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名或邮箱"
            required
            :disabled="loading"
          />
        </div>

        <!-- 注册时显示邮箱字段 -->
        <div v-if="!isLogin" class="form-group">
          <label for="email" class="form-label">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            placeholder="请输入邮箱地址"
            required
            :disabled="loading"
          />
        </div>

        <!-- 密码字段 -->
        <div class="form-group">
          <label for="password" class="form-label">密码</label>
          <div class="password-input-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入密码"
              required
              :disabled="loading"
            />
            <button
              type="button"
              class="password-toggle"
              @click="showPassword = !showPassword"
              :disabled="loading"
            >
              {{ showPassword ? '隐藏' : '显示' }}
            </button>
          </div>
        </div>

        <!-- 注册时显示确认密码字段 -->
        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword" class="form-label">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="form-input"
            placeholder="请再次输入密码"
            required
            :disabled="loading"
          />
        </div>

        <!-- 错误信息 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- 提交按钮 -->
        <button
          type="submit"
          class="submit-button"
          :disabled="loading || !isFormValid"
        >
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <!-- 切换登录/注册 -->
      <div class="login-footer">
        <p class="switch-mode">
          {{ isLogin ? '还没有账号？' : '已有账号？' }}
          <button
            type="button"
            class="switch-button"
            @click="toggleMode"
            :disabled="loading"
          >
            {{ isLogin ? '立即注册' : '立即登录' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/utils/auth.js'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const { login, register, isAuthenticated } = useAuth()

    // 响应式数据
    const isLogin = ref(true)
    const loading = ref(false)
    const error = ref('')
    const showPassword = ref(false)

    // 表单数据
    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      nickname: ''
    })

    // 计算属性
    const isFormValid = computed(() => {
      if (isLogin.value) {
        return form.value.username.trim() && form.value.password
      } else {
        return (
          form.value.username.trim() &&
          form.value.email.trim() &&
          form.value.password &&
          form.value.confirmPassword &&
          form.value.password === form.value.confirmPassword
        )
      }
    })

    // 方法
    const toggleMode = () => {
      isLogin.value = !isLogin.value
      error.value = ''
      // 清空表单
      form.value = {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        nickname: ''
      }
    }

    const handleSubmit = async () => {
      if (!isFormValid.value) return

      loading.value = true
      error.value = ''

      try {
        let result

        if (isLogin.value) {
          // 登录
          result = await login({
            username: form.value.username.trim(),
            password: form.value.password
          })
        } else {
          // 注册
          if (form.value.password !== form.value.confirmPassword) {
            error.value = '两次输入的密码不一致'
            return
          }

          result = await register({
            username: form.value.username.trim(),
            email: form.value.email.trim(),
            password: form.value.password,
            nickname: form.value.nickname.trim() || form.value.username.trim()
          })
        }

        if (result.success) {
          // 登录/注册成功，重定向
          const redirectPath = route.query.redirect || '/dashboard'
          router.push(redirectPath)
        } else {
          error.value = result.error
        }
      } catch (err) {
        error.value = err.message || '操作失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    // 生命周期
    onMounted(() => {
      // 如果已经登录，直接重定向
      if (isAuthenticated.value) {
        const redirectPath = route.query.redirect || '/dashboard'
        router.push(redirectPath)
      }
    })

    return {
      isLogin,
      loading,
      error,
      showPassword,
      form,
      isFormValid,
      toggleMode,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.login-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.form-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.password-input-wrapper {
  position: relative;
  display: flex;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  cursor: pointer;
  padding: 4px 8px;
}

.password-toggle:hover {
  color: #5a6fd8;
}

.password-toggle:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.error-message {
  background-color: #fee;
  color: #c53030;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 20px;
  border: 1px solid #fed7d7;
}

.submit-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
}

.switch-mode {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.switch-button {
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.switch-button:hover:not(:disabled) {
  color: #5a6fd8;
}

.switch-button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 24px;
  }
}
</style>