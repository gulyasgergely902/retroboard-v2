/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { defineStore } from 'pinia'
import type { Note, Category } from '@/services/board/types'
import type { Result } from '@/services/global/types'
import { $fetch } from '@/composables/fetch'
import { useAppService } from '@/services/app/app.service'

export const useBoardService = defineStore('board', {
  state: (): { notes: Note[]; categories: Category[]; selectedCategory: number | null } => ({
    notes: [],
    categories: [],
    selectedCategory: null,
  }),
  getters: {
    filteredNotes: (state) =>
      state.selectedCategory === -1
        ? state.notes
        : state.notes.filter((n) => n.category === state.selectedCategory),
  },
  actions: {
    async fetchBoardData(boardId: string) {
      this.selectedCategory = null
      try {
        await Promise.all([this.fetchNotes(boardId), this.fetchCategories(boardId, false)])
      } catch (err) {
        console.error('Error fetching board data:', err)
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

    async fetchCategories(boardId: string, selectedWasDeleted: boolean) {
      try {
        const response = await $fetch<Category[]>(`/api/categories?board_id=${boardId}`)
        this.categories = await response.json()
      } catch (err) {
        console.error('Error fetching categories:', err)
      } finally {
        if ((this.categories.length !== 0 && this.selectedCategory == null) || selectedWasDeleted) {
          this.selectedCategory = this.categories[0].id
        }
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

        await this.fetchNotes(boardId)

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
        await this.fetchNotes(boardId)
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
        const response = await $fetch<Result>(`/api/categories`, requestOptions)
        const result = await response.json()

        await this.fetchCategories(boardId, false)

        return result
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
        await this.fetchCategories(boardId, categoryId === this.selectedCategory)
      } catch (err) {
        console.error('Error deleting category ', categoryId, ', err:', err)
        throw err
      }
      if (this.categories.length === 0) {
        this.selectedCategory = null
      }
    },

    async exportData(boardId: string) {
      try {
        const response = await fetch(`/api/boards/export?board_id=${boardId}`)

        const disposition = response.headers.get('Content-Disposition')
        let filename = 'export.json'

        if (disposition) {
          const match = disposition.match(/filename="?([^"]+)"?/)
          if (match && match[1]) {
            filename = match[1]
          }
        }

        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        console.error('Error exporting board: ', err)
      }
    },

    async exportJson(boardId: string) {
      try {
        const response = await fetch(`/api/boards/export?board_id=${boardId}`)
        const json = await response.json()

        return JSON.stringify(json, null, 2)
      } catch (err) {
        console.error('Error exporting board to string: ', err)
        return ''
      }
    },

    async exportMarkdown(boardId: string) {
      try {
        const response = await fetch(`/api/boards/export?board_id=${boardId}`)
        const rawResponseData = await response.json()
        const boardName = rawResponseData['board_name']
        const categories: string[] = rawResponseData.notes.map((note) => note.category)

        let markdownString = '# ' + boardName + '\n\n'
        for (const category of [...new Set(categories)]) {
          markdownString += '## ' + category + '\n'
          for (const note of rawResponseData.notes) {
            if (note.category === category) {
              markdownString += '- ' + note.description + '\n'
            }
          }
          markdownString += '\n'
        }

        return markdownString
      } catch (err) {
        console.error('Error exporting board to markdown: ', err)
        return ''
      }
    },

    async importFromJson(rawContent: string) {
      interface ImportedNote {
        description: string
        category: string
        category_id: number
      }
      interface ImportedBoardData {
        board_name: string
        notes: ImportedNote[]
      }

      const jsonContent = JSON.parse(rawContent) as ImportedBoardData
      const boardName = jsonContent.board_name
      const boardNotes = jsonContent.notes
      const categories = [...new Set(boardNotes.map(note => note.category))]

      const appService = useAppService()
      const boardData = await appService.createNewBoard(boardName)
      const boardId_S = boardData.board_id?.toString() ?? "undefined"
      for (const category of categories) {
        const categoryData = await this.addCategory(boardId_S, category)
        const categoryId = categoryData?.category_id ?? 0
        console.log('Adding category', category, 'with id', categoryId)
        boardNotes.filter((note) => note.category === category).forEach((note) => {
          this.createNewNote(boardId_S, note.description, categoryId)
        })
      }
    },

    getCategoryNameById(categoryId: number) {
      return this.categories.find((n) => n.id === categoryId)?.name
    },

    async modifyNoteCategory(noteId: number, newCategory: number, boardId: string) {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category: newCategory }),
        }
        await $fetch<Result>(`/api/notes/` + noteId + `/category`, requestOptions)
        await this.fetchNotes(boardId)
      } catch (err) {
        console.error(
          'Error modifying category of note (id ',
          noteId,
          ') to category: ',
          newCategory,
          '(Err ',
          err,
          ')',
        )
      }
    },
  },
})
