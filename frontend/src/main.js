import './assets/main.css'
import './assets/theme.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { setupHttpInterceptors } from '@/utils/httpInterceptors.js'

// 初始化 HTTP 拦截器
setupHttpInterceptors()

const app = createApp(App)
app.use(router)
app.mount('#app')
