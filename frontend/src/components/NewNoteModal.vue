<template>
  <TransitionRoot
    as="template"
    :show="isModalOpen"
  >
    <Dialog
      class="relative z-10"
      @close="isModalOpen = false"
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
              class="relative transform overflow-hidden rounded-xl bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg"
            >
              <div class="bg-white dark:bg-slate-900 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                  <div
                    class="mx-auto flex size-12 shrink-0 items-center justify-center rounded-full bg-sky-200 sm:mx-0 sm:size-10"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="size-6 fill-sky-500"
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
                      class="text-gray-900 dark:text-white text-xl font-medium font-semibold"
                    >
                      Add Note
                    </DialogTitle>
                    <div class="mt-2">
                      <label
                        for="note_content"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                      >
                        Note Content
                      </label>
                      <textarea
                        id="note_content"
                        v-model="newNoteContent"
                        class="bg-gray-50 dark:bg-slate-800 text-gray-900 dark:text-white border-gray-300 dark:border-slate-700 dark:placeholder-slate-400 text-sm border rounded-lg block w-full p-2.5"
                        placeholder="Note content goes here..."
                        required
                      />
                      <label
                        for="note_category"
                        class="block mt-4 mb-2 text-sm font-medium text-gray-900 dark:text-white"
                      >
                        Note Category
                      </label>
                      <select
                        id="note_category"
                        v-model="newNoteCategory"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      >
                        <option
                          v-for="category in boardService.categories"
                          :key="category.id"
                          :value="category.id"
                        >
                          {{ category.name }}
                        </option>
                      </select>
                      <p
                        v-if="newNoteNameError"
                        class="text-red-500 text-sm"
                      >
                        Note content or category cannot be empty!
                      </p>
                      <p class="text-sm text-gray-900 dark:text-white">
                        Notes cannot be modified after creation!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-white dark:bg-slate-900 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button
                  type="button"
                  class="bg-sky-500 dark:bg-sky-900 text-sky-950 dark:text-sky-50 hover:bg-sky-600 dark:hover:bg-sky-950 transition-colors inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold sm:ml-3 sm:w-auto"
                  @click="createNote()"
                >
                  Create
                </button>
                <button
                  type="button"
                  class="bg-white dark:bg-slate-900 text-gray-900 dark:text-slate-50 hover:bg-gray-50 dark:hover:bg-slate-800 ring-slate-300 dark:ring-slate-800 transition-colors ring-inset mt-3 inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold shadow-xs ring-1 sm:mt-0 sm:w-auto"
                  @click="isModalOpen = false"
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
  const newNoteNameError = ref(false)
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

  const validateNewNoteContent = () => {
    if (!newNoteContent.value?.trim() || newNoteCategory.value == 0) {
      newNoteNameError.value = true
      return false
    } 
    newNoteNameError.value = false
    return true
  }

  function createNote() {
    if (validateNewNoteContent() && typeof newNoteContent.value === 'string') {
      boardService.createNewNote(props.currentBoardId, newNoteContent.value, newNoteCategory.value)
      newNoteContent.value = ''
      newNoteCategory.value = 0
      isModalOpen.value = false
    }
  }
</script>
