import { defineStore } from 'pinia'
import { view_states } from '@/enums/global.enums'

export const useGlobalService = defineStore('global', {
  state: (): { view_state: number } => ({
    view_state: view_states.home_view
  }),

  actions: {
    setViewState(target_view_state: number) {
        this.view_state = target_view_state
    }
  }
})
