import { createRouter, createWebHistory } from 'vue-router'
import WordBlast from '../components/WordBlast.vue'
import LevelSelect from '../pages/LevelSelect.vue'
import SectionSelect from '../pages/SectionSelect.vue'
import GamePanel from '../pages/GamePanel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WordBlast
    },
    {
      path: '/sections',
      name: 'sections',
      component: SectionSelect
    },
    {
      path: '/levels',
      name: 'levels',
      component: LevelSelect
    },
    {
      path: '/game/:levelId',
      name: 'game',
      component: GamePanel,
      props: true
    }
  ]
})

export default router