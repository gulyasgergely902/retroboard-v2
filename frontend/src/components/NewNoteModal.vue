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
  <TransitionRoot
    as="template"
    :show="isModalOpen"
  >
    <Dialog
      class="relative z-10"
      @close="closeModal()"
    >
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-500/75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg text-left shadow-xl transition-all sm:my-8 w-full sm:max-w-lg"
            >
              <div class="background-color px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                  <div
                    class="mx-auto flex size-12 shrink-0 items-center justify-center rounded-full icon-background sm:mx-0 sm:size-10"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="size-6 fill-[#579dff]"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                      />
                    </svg>
                  </div>
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <DialogTitle
                      as="h3"
                      class="text-color text-xl font-medium font-semibold"
                    >
                      Add Note
                    </DialogTitle>
                    <div class="mt-2">
                      <label
                        for="note_content"
                        class="block mb-2 text-sm font-medium text-color"
                      >
                        Note Content
                      </label>
                      <textarea
                        id="note_content"
                        v-model="newNoteContent"
                        @blur="validateNewNoteContent()"
                        class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
                        :class="{ 'input-error': newNoteContentError }"
                        placeholder="Note content goes here..."
                        required
                      />
                      <label
                        v-if="newNoteContentError"
                        for="note_content"
                        class="block mt-2 text-sm font-medium text-color-danger"
                      >
                        {{ newNoteContentError }}
                      </label>
                      <label
                        for="note_category"
                        class="block mt-4 mb-2 text-sm font-medium text-color"
                      >
                        Note Category
                      </label>
                      <select
                        id="note_category"
                        v-model="newNoteCategory"
                        @blur="validateNewNoteCategory()"
                        class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
                        :class="{ 'input-error': newNoteCategoryError }"
                      >
                        <option
                          v-for="category in boardService.categories"
                          :key="category.id"
                          :value="category.id"
                        >
                          {{ category.name }}
                        </option>
                      </select>
                      <label
                        v-if="newNoteCategoryError"
                        for="note_category"
                        class="block mt-2 text-sm font-medium text-color-danger"
                      >
                        {{ newNoteCategoryError }}
                      </label>
                      <p class="text-sm text-gray-900 dark:text-white">
                        Notes cannot be modified after creation!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="background-color px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button
                  type="button"
                  class="button-color-primary text-color-over-primary transition-colors inline-flex w-full justify-center rounded-sm px-3 py-2 text-sm font-semibold sm:ml-3 sm:w-auto cursor-pointer"
                  @click="createNote()"
                >
                  Create
                </button>
                <button
                  type="button"
                  class="background-color text-color transition-colors mt-3 inline-flex w-full justify-center rounded-sm px-3 py-2 text-sm font-semibold shadow-xs sm:mt-0 sm:w-auto cursor-pointer"
                  @click="closeModal()"
                  ref="cancelButtonRef"
                >
                  Cancel
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useBoardService } from '@/services/board/board.service'
  const newNoteContent = ref('')
  const newNoteCategory = ref(0)
  const newNoteContentError = ref('')
  const newNoteCategoryError = ref('')

  const isModalOpen = defineModel<boolean>('isModalOpen')
  const props = defineProps(['currentBoardId'])
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'

  const boardService = useBoardService()

  function validateNewNoteContent() {
    if (!newNoteContent.value.trim()) {
      newNoteContentError.value = 'This field cannot be empty!'
      return false
    }
    if (typeof newNoteContent.value !== 'string') {
      newNoteContentError.value = 'Note can only contain text!'
      return false
    }
    newNoteContentError.value = ''
    return true
  }

  function validateNewNoteCategory() {
    if (newNoteCategory.value === 0) {
      newNoteCategoryError.value = 'You must select a category!'
      return false
    }
    newNoteCategoryError.value = ''
    return true
  }

  function validateAll() {
    const validators = [validateNewNoteContent, validateNewNoteCategory]
    let allValid = true

    for (const validator of validators) {
      if (!validator()) {
        allValid = false
      }
    }

    return allValid
  }

  function createNote() {
    if (validateAll()) {
      boardService.createNewNote(props.currentBoardId, newNoteContent.value, newNoteCategory.value)
      newNoteContent.value = ''
      newNoteCategory.value = 0
      isModalOpen.value = false
    }
  }

  function closeModal() {
    isModalOpen.value = false
    newNoteContent.value = ''
    newNoteCategory.value = 0
    newNoteContentError.value = ''
    newNoteCategoryError.value = ''
  }
</script>
