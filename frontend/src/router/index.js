import { createRouter, createWebHistory } from 'vue-router'
import WordBlast from '@/components/WordBlast.vue'
import LevelSelect from '@/pages/LevelSelect.vue'
import SectionSelect from '@/pages/SectionSelect.vue'
import GamePanel from '@/pages/GamePanel.vue'
import GameConfig from '@/pages/GameConfig.vue'
import Login from '@/pages/Login.vue'

import Profile from '@/pages/Profile.vue'
import UserProfile from '@/pages/UserProfile.vue'
import Settings from '@/pages/Settings.vue'
import VocabularyManagement from '@/pages/VocabularyManagement.vue'
import { useAuth } from '@/utils/auth.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { 
        requiresAuth: false,
        hideForAuth: true,
        title: '用户登录'
      }
    },
    {
      path: '/',
      name: 'home',
      redirect: '/game'
    },
    {
      path: '/game',
      name: 'wordblast',
      component: WordBlast,
      meta: { 
        requiresAuth: true,
        title: '单词爆破'
      }
    },
    {
      path: '/sections',
      name: 'sections',
      component: SectionSelect,
      meta: { 
        requiresAuth: true,
        title: '选择章节'
      }
    },
    {
      path: '/levels',
      name: 'levels',
      component: LevelSelect,
      meta: { 
        requiresAuth: true,
        title: '选择关卡'
      }
    },
    {
      path: '/game/:levelId',
      name: 'game',
      component: GamePanel,
      props: true,
      meta: { 
        requiresAuth: true,
        title: '游戏中'
      }
    },
    {
      path: '/config',
      name: 'config',
      component: GameConfig,
      meta: { 
        requiresAuth: true,
        title: '游戏配置'
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserProfile,
      meta: { 
        requiresAuth: true,
        title: '个人资料'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings,
      meta: { 
        requiresAuth: false,
        title: '游戏设置'
      }
    },
    {
      path: '/vocabulary',
      name: 'vocabulary',
      component: VocabularyManagement,
      meta: { 
        requiresAuth: true,
        title: '词汇管理'
      }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const hideForAuth = to.matched.some(record => record.meta.hideForAuth)

  if (requiresAuth && !isAuthenticated.value) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  if (hideForAuth && isAuthenticated.value) {
    next('/game')
    return
  }

  next()
})

export default router