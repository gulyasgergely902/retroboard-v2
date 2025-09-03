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
                        class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
                        :class="{ 'input-error': newNoteContentError }"
                        placeholder="Note content goes here..."
                        required
                      />
                      <SelectInputComponent
                        label="Note Category"
                        description="Pick a category for this note."
                        :options="boardService.categories"
                        v-model:selection="newNoteCategory"
                        v-model:error="newNoteCategoryError"
                      />
                      <p class="text-sm text-gray-900 dark:text-white">
                        Notes cannot be modified after creation!
                      </p>
                      <div
                        v-if="errorMessage"
                        class="background-color-danger text-color-over-primary rounded-sm px-2 py-1 mt-4"
                      >
                        {{ errorMessage }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="background-color px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <ButtonInputComponent
                  class="w-full justify-center mt-3 sm:mt-0 sm:ml-3 sm:w-auto"
                  @click="createNote()"
                  label="Create"
                  variant="primary"
                />
                <ButtonInputComponent
                  class="w-full justify-center mt-3 sm:mt-0 sm:w-auto"
                  @click="closeModal()"
                  label="Cancel"
                  variant="outline"
                />
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
  import { useLocalStorage } from '@vueuse/core'
  import { useBoardService } from '@/services/board/board.service'
  import SelectInputComponent from '@/components/input/SelectInputComponent.vue'
  import ButtonInputComponent from '@/components/input/ButtonInputComponent.vue'
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'

  const errorMessage = ref('')
  const newNoteContent = useLocalStorage('newNoteContent', '')
  const newNoteCategory = useLocalStorage('newNoteCategory', 0)
  const newNoteContentError = ref(false)
  const newNoteCategoryError = ref(false)

  const isModalOpen = defineModel<boolean>('isModalOpen')

  const props = defineProps(['currentBoardId'])

  const boardService = useBoardService()

  function validateNewNoteContent() {
    if (!newNoteContent.value.trim()) {
      newNoteContentError.value = true
      return false
    }
    if (typeof newNoteContent.value !== 'string') {
      newNoteContentError.value = true
      return false
    }
    newNoteContentError.value = false
    return true
  }

  function validateNewNoteCategory() {
    if (newNoteCategory.value === 0) {
      newNoteCategoryError.value = true
      return false
    }
    newNoteCategoryError.value = false
    return true
  }

  function validateAll() {
    const validators = [validateNewNoteContent, validateNewNoteCategory]
    let allValid = true

    for (const validator of validators) {
      if (!validator()) {
        allValid = false
        errorMessage.value = 'Fill all required fields!'
      }
    }

    return allValid
  }

  async function createNote() {
    if (!validateAll()) return

    try {
      await boardService.createNewNote(
        props.currentBoardId,
        newNoteContent.value,
        newNoteCategory.value,
      )

      newNoteContent.value = ''
      newNoteCategory.value = 0
      closeModal()
    } catch (err) {
      console.error('Error while creating note:', err)
      errorMessage.value = 'Error creating note'
    }
  }

  function closeModal() {
    isModalOpen.value = false
    newNoteContentError.value = false
    newNoteCategoryError.value = false
    errorMessage.value = ''
  }
</script>
