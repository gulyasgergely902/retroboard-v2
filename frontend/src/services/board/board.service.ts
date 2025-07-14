import { defineStore } from 'pinia'
import type { Note, Category } from '@/services/app/types'
import { $fetch } from '@/composables/fetch'

export const useBoardService = defineStore('board', {
  state: (): { notes: Note[]; categories: Category[]; selectedCategory: number | null } => ({
    notes: [],
    categories: [],
    selectedCategory: null,
  }),
  getters: {
    filteredNotes: (state) => state.notes.filter((n) => n.category === state.selectedCategory),
  },
  actions: {
    async fetchBoardData(boardId: string) {
      try {
        await Promise.all([this.fetchNotes(boardId), this.fetchCategories(boardId)])
      } catch (err) {
        console.error('Error fetching board data:', err)
      } finally {
        if (this.categories.length === 0) {
          this.selectedCategory = null
        }

        this.selectedCategory = this.categories[0].id
      }
    },

    async fetchNotes(boardId: string) {
      try {
        const response = await $fetch<Note[]>(`/api/notes?board_id=${boardId}`)
        this.notes = await response.json()
      } catch (err) {
        console.error('Error fetching notes:', err)
      }
    },

    async fetchCategories(boardId: string) {
      try {
        const response = await $fetch<Category[]>(`/api/categories?board_id=${boardId}`)
        this.categories = await response.json()
      } catch (err) {
        console.error('Error fetching categories:', err)
      }
    },
  },
})
