import { defineStore } from 'pinia'
import type { Note, Category } from '@/services/board/types'
import type { Result } from '@/services/global/types'
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

    async createNewNote(boardId: string, noteContent: string, noteCategory: number) {
      if (noteContent.length === 0 || noteCategory === 0) {
        console.error('Empty note content or category')
        throw new Error('Empty note content or category')
      }
      try {
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            description: noteContent,
            category: noteCategory,
            tags: [],
            board_id: boardId,
          }),
        }
        const response = await $fetch<Result>(`/api/notes`, requestOptions)
        const result = await response.json

        await this.fetchBoardData(boardId)

        return result
      } catch (err) {
        console.error('Error creating new note:', err)
      }
    },

    async removeNote(boardId: string, noteId: number) {
      if (noteId === 0) {
        console.error('Note id cannot be 0')
        throw new Error('Note id cannot be 0')
      }
      try {
        const requestOptions = {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        }
        await $fetch<Result>(`/api/notes?note_id=${noteId}`, requestOptions)
        await this.fetchBoardData(boardId)
      } catch (err) {
        console.error('Error deleting note ', noteId, ', err:', err)
      }
    },

    async addCategory(boardId: string, categoryName: string) {
      try {
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: categoryName, board_id: boardId }),
        }
        await $fetch<Result>(`/api/categories`, requestOptions)
        await this.fetchCategories(boardId)
      } catch (err) {
        console.error('Error adding category ', categoryName, ', err:', err)
      }
    },

    async removeCategory(boardId: string, categoryId: number) {
      try {
        const requestOptions = {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        }
        await $fetch<Result>(`/api/categories?category_id=${categoryId}`, requestOptions)
        await this.fetchCategories(boardId)
      } catch (err) {
        console.error('Error deleting category ', categoryId, ', err:', err)
      }
    }
  },
})
