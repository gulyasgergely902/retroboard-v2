import { defineStore } from 'pinia'
import type { Board } from '@/services/board/types'
import { $fetch } from '@/composables/fetch'

export const useAppService = defineStore('app', {
  state: (): { loading: boolean; boards: Board[] } => ({
    loading: true,
    boards: [],
  }),

  actions: {
    async fetchBoards() {
      try {
        this.loading = true
        const response = await $fetch<Board[]>('/api/boards')
        this.boards = await response.json()
        this.loading = false
      } catch (err) {
        console.error('Error fetching boards:', err)
      } finally {
        this.loading = false
      }
    },
  },
})
