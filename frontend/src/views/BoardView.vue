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
    <NewNoteModal
      v-model:is-modal-open="isModalOpen"
      :current-board-id="boardId"
    />
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
      <div
        class="bg-white dark:bg-sky-900 text-sky-950 dark:text-sky-50 border border-gray-200 dark:border-sky-800 rounded-xl p-4"
      >
        <div class="flex justify-end">
          <button
            class="inline-block text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-1.5"
            type="button"
            @click="boardService.removeNote(boardId, item.id)"
          >
            <span class="sr-only">Open dropdown</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-4 fill-gray-300"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
              />
            </svg>
          </button>
        </div>
        <div class="flex flex-col pb-7 ps-2">
          <span>{{ item.description }}</span>
        </div>
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
  const boardId = ref('')
  if (Array.isArray(route.params.id)) {
    boardId.value = route.params.id[0]
  } else {
    boardId.value = route.params.id
  }
  const boardService = useBoardService()
  const visibilityChecked = useLocalStorage('visibilityChecked', false)

  const isModalOpen = ref(false)

  void boardService.fetchBoardData(boardId.value as string)
</script>
