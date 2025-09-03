<!--
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<template>
  <NewNoteModal
    v-model:is-modal-open="isNewNoteModalOpen"
    :current-board-id="boardId"
  />
  <BoardSettingsModal
    v-model:is-modal-open="isBoardSettingsModalOpen"
    :current-board-id="boardId"
  />
  <EditNoteCategoryModal
    v-model:is-modal-open="isEditNoteCategoryModalOpen"
    :current-board-id="boardId"
    :note-id="selectedNoteId"
  />
  <div class="background-color-bold pt-4 rounded-lg w-full">
    <div class="flex content-center h-8 px-2 w-full">
      <span class="text-color ms-1 text-xl font-medium">
        {{ appService.boardName }}
      </span>
    </div>
    <div class="flex w-full flex-col md:flex-row items-center justify-between mx-auto px-3">
      <div class="max-w-full md:basis-2/3 md:max-w-[66.666%] max-w-3xl w-auto">
        <FilterToggle
          class="flex-auto"
          :categories="boardService.categories"
          v-model:categoryToHighlight="boardService.selectedCategory"
        />
      </div>
      <div
        class="max-w-full mt-4 md:mt-0 md:basis-1/3 md:shrink-0 md:min-w-[33.333%] flex items-center sm:justify-end"
      >
        <Toggle
          class="flex-none"
          label="Privacy mode"
          alignment="left"
          v-model="visibilityChecked"
        />
        <ButtonInputComponent
          class="ml-2 mr-2"
          @click="isBoardSettingsModalOpen = true"
          variant="icon"
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
        </ButtonInputComponent>
        <ButtonInputComponent
          class="ml-2"
          @click="isNewNoteModalOpen = true"
          :label="newNoteButtonLabel"
          variant="primary"
        />
      </div>
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
          class="background-color text-color transition-colors p-4 rounded-md border-color border-color-hover border-1"
          :class="{ 'blur-sm': visibilityChecked }"
        >
          <div class="flex justify-end">
            <div
              class="background-color-bold rounded-sm border-1 border-color inline-flex items-center"
            >
              <ButtonInputComponent
                class="inline-block p-1.5"
                @click="openEditNoteCategoryModal(item.id)"
                variant="icon"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-4"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M13.5 8H4m4 6h8m0 0-2-2m2 2-2 2M4 6v13a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-5.032a1 1 0 0 1-.768-.36l-1.9-2.28a1 1 0 0 0-.768-.36H5a1 1 0 0 0-1 1Z"
                  />
                </svg>
              </ButtonInputComponent>
              <div class="inline-block self-stretch vertical-separator separator-width"></div>
              <ButtonInputComponent
                class="inline-block p-1.5"
                @click="openConfirmModal(item.id)"
                variant="icon_danger"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-4"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                  />
                </svg>
              </ButtonInputComponent>
            </div>
          </div>
          <div class="flex flex-col pb-7 ps-2">
            <p class="text-color text-lg">{{ item.description }}</p>
            <p
              v-if="boardService.selectedCategory === -1"
              class="background-color-primary text-color-over-primary text-xs inline-block max-w-max rounded-full py-1 px-2 mt-2"
            >
              {{ boardService.getCategoryNameById(item.category) }}
            </p>
          </div>
        </div>
      </template>
    </MasonryWall>
    <YesNoModal
      v-model:is-modal-open="isYesNoModalOpen"
      @answer="handleRemoveNote"
      label="Are you sure?"
      description="This action is irreversible!"
      positiveActionLabel="Yes"
      negativeActionLabel="Cancel"
      danger
    />
  </div>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import { useLocalStorage } from '@vueuse/core'
  import { useAppService } from '@/services/app/app.service'
  import { useBoardService } from '@/services/board/board.service'
  import MasonryWall from '@yeger/vue-masonry-wall'
  import FilterToggle from '@/components/FilterToggle.vue'
  import Toggle from '@/components/Toggle.vue'

  import NewNoteModal from '@/components/modals/NewNoteModal.vue'
  import BoardSettingsModal from '@/components/modals/BoardSettingsModal.vue'
  import YesNoModal from '@/components/modals/YesNoModal.vue'

  import EditNoteCategoryModal from '@/components/modals/EditNoteCategoryModal.vue'
  import ButtonInputComponent from '@/components/input/ButtonInputComponent.vue'

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

  const noteDraft = useLocalStorage<string>('newNoteContent', '')

  const isNewNoteModalOpen = ref(false)
  const isBoardSettingsModalOpen = ref(false)
  const isYesNoModalOpen = ref(false)
  const isEditNoteCategoryModalOpen = ref(false)

  const newNoteButtonLabel = ref('')

  void appService.getBoardNameById(boardId.value as string)
  void boardService.fetchBoardData(boardId.value as string)

  const selectedNoteId = ref(0)
  function selectNoteId(noteId: number) {
    selectedNoteId.value = noteId
  }

  function openConfirmModal(noteId: number) {
    selectNoteId(noteId)
    isYesNoModalOpen.value = true
  }

  function openEditNoteCategoryModal(noteId: number) {
    selectNoteId(noteId)
    isEditNoteCategoryModalOpen.value = true
  }

  function handleRemoveNote(answer: boolean) {
    if (answer) {
      boardService.removeNote(boardId.value, selectedNoteId.value)
    }
  }

  watch(
    noteDraft,
    (draftContent) => {
      if (draftContent.trim().length > 0) {
        newNoteButtonLabel.value = 'Resume Draft'
      } else {
        newNoteButtonLabel.value = 'New Note'
      }
    },
    { immediate: true },
  )
</script>
