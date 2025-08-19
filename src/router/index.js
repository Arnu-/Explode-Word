import { createRouter, createWebHistory } from 'vue-router'
import WordBlast from '../components/WordBlast.vue'
import LevelSelect from '../pages/LevelSelect.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WordBlast
    },
    {
      path: '/levels',
      name: 'levels',
      component: LevelSelect
    }
  ]
})

export default router