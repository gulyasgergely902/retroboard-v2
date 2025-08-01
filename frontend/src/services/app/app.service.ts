import { defineStore } from 'pinia'
import type { Board } from '@/services/app/types'
import type { Result } from '@/services/global/types'
import { $fetch } from '@/composables/fetch'
import router from '@/router/'

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

    getBoardNameById(id: string): string | undefined {
      const numericId = Number(id)
      if (isNaN(numericId)) return undefined
      return this.boards.find((board) => board.id === numericId)?.name
    },

    async createNewBoard(boardTitle: string) {
      if (boardTitle.length === 0) {
        console.error('Empty board name')
        throw new Error('Empty board name')
      }
      try {
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: boardTitle }),
        }
        const response = await $fetch<Result>(`/api/boards`, requestOptions)
        const result = await response.json()

        await this.fetchBoards()

        return result
      } catch (err) {
        console.error('Error creating new board:', err)
      }
    },

    async removeBoard(boardId: number) {
      if (boardId === 0) {
        console.error('Note id cannot be 0')
        throw new Error('Note id cannot be 0')
      }
      try {
        const requestOptions = {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        }
        await $fetch<Result>(`/api/boards?board_id=${boardId}`, requestOptions)
        router.push('/')
      } catch (err) {
        console.error('Error deleting board ', boardId, ', err:', err)
      }
    },
  },
})
