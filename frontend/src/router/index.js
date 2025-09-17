import { createRouter, createWebHistory } from 'vue-router'
import WordBlast from '../components/WordBlast.vue'
import LevelSelect from '../pages/LevelSelect.vue'
import SectionSelect from '../pages/SectionSelect.vue'
import GamePanel from '../pages/GamePanel.vue'
import GameConfig from '../pages/GameConfig.vue'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import Profile from '../pages/Profile.vue'
import VocabularyManagement from '../pages/VocabularyManagement.vue'
import { authManager } from '../utils/auth.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { 
        requiresAuth: false,
        hideForAuth: true
      }
    },
    {
      path: '/',
      name: 'home',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/game',
      name: 'wordblast',
      component: WordBlast,
      meta: { requiresAuth: true }
    },
    {
      path: '/sections',
      name: 'sections',
      component: SectionSelect,
      meta: { requiresAuth: true }
    },
    {
      path: '/levels',
      name: 'levels',
      component: LevelSelect,
      meta: { requiresAuth: true }
    },
    {
      path: '/game/:levelId',
      name: 'game',
      component: GamePanel,
      props: true,
      meta: { requiresAuth: true }
    },
    {
      path: '/config',
      name: 'config',
      component: GameConfig,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/vocabulary',
      name: 'vocabulary',
      component: VocabularyManagement,
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = authManager.isAuthenticated
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const hideForAuth = to.matched.some(record => record.meta.hideForAuth)

  if (requiresAuth && !isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  if (hideForAuth && isAuthenticated) {
    next('/dashboard')
    return
  }

  next()
})

export default router