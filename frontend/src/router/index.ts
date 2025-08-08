import { createRouter, createWebHistory } from 'vue-router'
import BoardsView from '@/views/BoardsView.vue'
import NotesView from '@/views/NotesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'boards',
      component: BoardsView,
    },
    {
      path: '/board/:id',
      name: 'board',
      component: NotesView,
    },
  ],
})

export default router
