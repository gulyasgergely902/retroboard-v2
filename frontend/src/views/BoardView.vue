<template>
  <div class="max-w-screen-xl flex items-center justify-between mx-auto px-4">
    <FilterToggle
      class="flex-auto"
      :categories="boardService.categories"
      v-model:categoryToHighlight="boardService.selectedCategory"
    />
    <Toggle
      class="flex-none"
      label="Privacy mode"
      alignment="left"
      v-model="visibilityChecked"
    />
    <button
      type="button"
      class="bg-sky-500 dark:bg-sky-900 text-sky-950 dark:text-sky-50 hover:bg-sky-600 dark:hover:bg-sky-950 transition-colors ml-auto inline-flex items-center min-w-fit gap-x-2 rounded-xl px-4 py-2 text-sm font-semibold cursor-pointer"
      @click="isModalOpen = true"
      >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-5"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 4.5v15m7.5-7.5h-15"
        />
      </svg>

      New Note
    </button>
    <NewNoteModal v-model:is-modal-open="isModalOpen" :current-board-id="route.params.id"/>
  </div>
  <MasonryWall
    :items="boardService.filteredNotes"
    :ssr-columns="1"
    :column-width="300"
    :gap="16"
    class="p-4"
    :class="{ 'blur-sm': visibilityChecked }"
  >
    <template #default="{ item }">
      <div class="bg-sky-500 dark:bg-sky-900 text-sky-950 dark:text-sky-50 rounded-xl p-4">
        <span>{{ item.description }}</span>
      </div>
    </template>
  </MasonryWall>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useLocalStorage } from '@vueuse/core'
  import { useBoardService } from '@/services/board/board.service'
  import MasonryWall from '@yeger/vue-masonry-wall'
  import FilterToggle from '@/components/FilterToggle.vue'
  import Toggle from '@/components/Toggle.vue'
  import NewNoteModal from '@/components/NewNoteModal.vue'

  const route = useRoute()
  const boardService = useBoardService()
  const visibilityChecked = useLocalStorage('visibilityChecked', false)

  const isModalOpen = ref(false)

  void boardService.fetchBoardData(route.params.id as string)
</script>
