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
import type { Board, Setting } from '@/services/app/types'
import type { Result } from '@/services/global/types'
import { $fetch } from '@/composables/fetch'
import router from '@/router/'

export const useAppService = defineStore('app', {
  state: (): { loading: boolean; boards: Board[]; settings: Setting[] } => ({
    loading: true,
    boards: [],
    settings: [],
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

    async fetchSettings() {
      try {
        const response = await $fetch<Setting[]>(`/api/settings`)
        const data = await response.json()

        this.settings = data.map((setting) => {
          if (setting.setting_type === 'boolean') {
            return { ...setting, setting_value: (setting.setting_value =="1") }
          }
          return setting
        })
      } catch (err) {
        console.error('Error fetching settings:', err)
      }
    },

    async saveSettings() {
      for (const setting of [...this.settings]) {
        try {
          const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_value: setting.setting_value }),
          }
          const endpoint = `/api/settings/` + setting.setting_name
          await $fetch<Result>(endpoint, requestOptions)
        } catch (err) {
          console.error('Error saving settings:', err)
        }
      }
    },
  },
})
