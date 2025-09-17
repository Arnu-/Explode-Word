<template>
  <div v-if="isChecking" class="auth-checking">
    <div class="loading-spinner">
      <div class="spinner"></div>
      <p>验证登录状态...</p>
    </div>
  </div>
  <div v-else-if="authError" class="auth-error">
    <div class="error-message">
      <h3>认证失败</h3>
      <p>{{ authError }}</p>
      <button @click="redirectToLogin" class="login-btn">
        重新登录
      </button>
    </div>
  </div>
  <slot v-else />
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuth } from '@/utils/auth.js'
import { checkAuthStatus } from '@/utils/routeGuard.js'

export default {
  name: 'AuthCheck',
  setup() {
    const { isAuthenticated } = useAuth()
    const isChecking = ref(true)
    const authError = ref(null)

    const redirectToLogin = () => {
      window.location.href = '/login'
    }

    onMounted(async () => {
      try {
        if (!isAuthenticated.value) {
          authError.value = '用户未登录'
          isChecking.value = false
          return
        }

        // 检查认证状态
        const isValid = await checkAuthStatus()
        if (!isValid) {
          authError.value = '登录状态已过期，请重新登录'
        }
      } catch (error) {
        console.error('认证检查失败:', error)
        authError.value = '认证检查失败，请重新登录'
      } finally {
        isChecking.value = false
      }
    })

    return {
      isChecking,
      authError,
      redirectToLogin
    }
  }
}
</script>

<style scoped>
.auth-checking {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.loading-spinner {
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.auth-error {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.error-message {
  text-align: center;
  padding: 32px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.error-message h3 {
  color: #dc3545;
  margin-bottom: 16px;
}

.error-message p {
  color: #6c757d;
  margin-bottom: 24px;
}

.login-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background: #0056b3;
}
</style>