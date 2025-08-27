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
                        d="M13.5 8H4m4 6h8m0 0-2-2m2 2-2 2M4 6v13a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-5.032a1 1 0 0 1-.768-.36l-1.9-2.28a1 1 0 0 0-.768-.36H5a1 1 0 0 0-1 1Z"
                      />
                    </svg>
                  </div>
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <DialogTitle
                      as="h3"
                      class="text-color text-xl font-medium font-semibold"
                    >
                      Edit Note Category
                    </DialogTitle>
                    <div class="mt-2">
                      <SelectInputComponent
                        label="New Note Category"
                        description="Pick a category to move the note into."
                        :options="boardService.categories"
                        v-model:selection="newNoteCategory"
                        v-model:error="newNoteCategoryError"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div class="background-color px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <ButtonInputComponent
                  class="w-full justify-center mt-3 sm:mt-0 sm:ml-3 sm:w-auto"
                  @click="modifyNoteCategory()"
                  label="Move"
                  primary
                />
                <ButtonInputComponent
                  class="w-full justify-center mt-3 sm:mt-0 sm:w-auto"
                  @click="closeModal()"
                  label="Cancel"
                  outline
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
  import { useBoardService } from '@/services/board/board.service'
  import SelectInputComponent from './input/SelectInputComponent.vue'
  import ButtonInputComponent from './input/ButtonInputComponent.vue'
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'

  const newNoteCategory = ref(0)
  const newNoteCategoryError = ref('')

  const isModalOpen = defineModel<boolean>('isModalOpen')

  const props = defineProps(['currentBoardId', 'noteId'])

  const boardService = useBoardService()

  function validateNewNoteCategory() {
    if (newNoteCategory.value === 0) {
      newNoteCategoryError.value = 'You must select a category!'
      return false
    }
    newNoteCategoryError.value = ''
    return true
  }

  function validateAll() {
    const validators = [validateNewNoteCategory]
    let allValid = true

    for (const validator of validators) {
      if (!validator()) {
        allValid = false
      }
    }

    return allValid
  }

  function modifyNoteCategory() {
    if (validateAll()) {
      boardService.modifyNoteCategory(props.noteId, newNoteCategory.value, props.currentBoardId)
      newNoteCategory.value = 0
      closeModal()
    }
  }

  function closeModal() {
    isModalOpen.value = false
    newNoteCategory.value = 0
    newNoteCategoryError.value = ''
  }
</script>
