import { defineStore } from 'pinia'
import type { Board, Result } from '@/services/app/types'
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

    async createNewBoard(boardTitle: string) {
      if (boardTitle.length === 0) {
        console.error("Empty board name")
        throw new Error("Empty board name")
      }
      try {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: boardTitle })
        };
        const response = await $fetch<Result>(`/api/boards`, requestOptions)
        const result = await response.json

        await this.fetchBoards()

        return result
      } catch (err) {
        console.error('Error creating new board:', err)
      }
    },
  },
})
