<template>
  <div class="background-color-bold pt-4 rounded-lg w-full">
    <div class="flex content-center h-8 px-2 w-full">
      <span class="text-color ms-1 text-xl font-medium">
        {{ appService.getBoardNameById(boardId) }}
      </span>
    </div>
    <div class="max-w-screen-xl flex items-center justify-between mx-auto px-3">
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
        class="background-color-primary text-color-over-primary transition-colors ml-auto inline-flex items-center gap-x-2 rounded-sm px-3 py-2 text-sm mr-2 font-semibold cursor-pointer"
        @click="isBoardSettingsModalOpen = true"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="size-5"
        >
          <path
            fill-rule="evenodd"
            d="M11.828 2.25c-.916 0-1.699.663-1.85 1.567l-.091.549a.798.798 0 0 1-.517.608 7.45 7.45 0 0 0-.478.198.798.798 0 0 1-.796-.064l-.453-.324a1.875 1.875 0 0 0-2.416.2l-.243.243a1.875 1.875 0 0 0-.2 2.416l.324.453a.798.798 0 0 1 .064.796 7.448 7.448 0 0 0-.198.478.798.798 0 0 1-.608.517l-.55.092a1.875 1.875 0 0 0-1.566 1.849v.344c0 .916.663 1.699 1.567 1.85l.549.091c.281.047.508.25.608.517.06.162.127.321.198.478a.798.798 0 0 1-.064.796l-.324.453a1.875 1.875 0 0 0 .2 2.416l.243.243c.648.648 1.67.733 2.416.2l.453-.324a.798.798 0 0 1 .796-.064c.157.071.316.137.478.198.267.1.47.327.517.608l.092.55c.15.903.932 1.566 1.849 1.566h.344c.916 0 1.699-.663 1.85-1.567l.091-.549a.798.798 0 0 1 .517-.608 7.52 7.52 0 0 0 .478-.198.798.798 0 0 1 .796.064l.453.324a1.875 1.875 0 0 0 2.416-.2l.243-.243c.648-.648.733-1.67.2-2.416l-.324-.453a.798.798 0 0 1-.064-.796c.071-.157.137-.316.198-.478.1-.267.327-.47.608-.517l.55-.091a1.875 1.875 0 0 0 1.566-1.85v-.344c0-.916-.663-1.699-1.567-1.85l-.549-.091a.798.798 0 0 1-.608-.517 7.507 7.507 0 0 0-.198-.478.798.798 0 0 1 .064-.796l.324-.453a1.875 1.875 0 0 0-.2-2.416l-.243-.243a1.875 1.875 0 0 0-2.416-.2l-.453.324a.798.798 0 0 1-.796.064 7.462 7.462 0 0 0-.478-.198.798.798 0 0 1-.517-.608l-.091-.55a1.875 1.875 0 0 0-1.85-1.566h-.344ZM12 15.75a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5Z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
      <button
        type="button"
        class="background-color-primary text-color-over-primary transition-colors ml-auto inline-flex items-center gap-x-2 rounded-sm px-3 py-2 text-sm font-semibold cursor-pointer"
        @click="isNewNoteModalOpen = true"
      >
        New Note
      </button>
      <NewNoteModal
        v-model:is-modal-open="isNewNoteModalOpen"
        :current-board-id="boardId"
      />
    </div>
    <MasonryWall
      :items="boardService.filteredNotes"
      :ssr-columns="1"
      :column-width="300"
      :gap="16"
      class="p-2"
    >
      <template #default="{ item }">
        <div
          class="background-color text-color transition-colors p-4 rounded-md border-color border-1"
          :class="{ 'blur-sm': visibilityChecked }"
        >
          <div class="flex justify-end">
            <button
              class="inline-block text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-1.5"
              type="button"
              @click="boardService.removeNote(boardId, item.id)"
            >
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
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useLocalStorage } from '@vueuse/core'
  import { useAppService } from '@/services/app/app.service'
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
  const appService = useAppService()
  const boardService = useBoardService()
  const visibilityChecked = useLocalStorage('visibilityChecked', false)

  const isNewNoteModalOpen = ref(false)
  const isBoardSettingsModalOpen = ref(false)

  void boardService.fetchBoardData(boardId.value as string)
</script>
