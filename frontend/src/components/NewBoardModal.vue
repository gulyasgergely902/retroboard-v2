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
                        d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z"
                      />
                    </svg>
                  </div>
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <DialogTitle
                      as="h3"
                      class="text-color text-xl font-medium font-semibold"
                    >
                      Create Board
                    </DialogTitle>
                    <div class="mt-2">
                      <TextInputComponent
                        label="Board Name"
                        description="A descriptive name for the new board, e.g. Backend Team Retrospective."
                        v-model:textContent="newBoardName"
                        v-model:error="newBoardNameError"
                      />
                      <CheckboxInputComponent
                        label="Create default categories"
                        description="Choose a board category template to initialize your board with."
                        v-model:checkedState="initializeWithCategories"
                      />
                      <div
                        v-if="initializeWithCategories"
                        class="ms-2 text-sm mt-2"
                      >
                        <label
                          for="initial_category"
                          class="font-medium text-color"
                        >
                          Templates
                        </label>
                        <select
                          id="initial_category"
                          v-model="selectedCategoryTemplateId"
                          @blur="validateSelectedTemplate()"
                          class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
                          :class="{ 'input-error': noSelectedTemplateError }"
                        >
                          <option
                            v-for="template in templates"
                            :key="template.id"
                            :value="template.id"
                          >
                            {{ template.templateName }}
                          </option>
                        </select>
                        <label
                          v-if="noSelectedTemplateError"
                          for="note_category"
                          class="block mt-2 text-sm font-medium text-color-danger"
                        >
                          {{ noSelectedTemplateError }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="background-color px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button
                  type="button"
                  class="button-color-primary text-color-over-primary transition-colors inline-flex w-full justify-center rounded-sm px-3 py-2 text-sm font-semibold sm:ml-3 sm:w-auto cursor-pointer"
                  @click="createBoard()"
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
  import { useAppService } from '@/services/app/app.service'
  import { useBoardService } from '@/services/board/board.service'
  const newBoardName = ref('')
  const newBoardNameError = ref('')
  const initializeWithCategories = ref(false)
  const selectedCategoryTemplateId = ref(0)
  const noSelectedTemplateError = ref('')

  const isModalOpen = defineModel<boolean>('isModalOpen')
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'
  import CheckboxInputComponent from './input/CheckboxInputComponent.vue'
  import TextInputComponent from './input/TextInputComponent.vue'

  interface BoardCategoriesTemplate {
    id: number
    templateName: string
    categories: string[]
  }

  const templates = ref<BoardCategoriesTemplate[]>([
    {
      id: 1,
      templateName: 'Retrospective (Good, Bad, Actions)',
      categories: ['Went well', 'Needs improvement', 'Action items'],
    },
    {
      id: 2,
      templateName: 'Team Centric (Liked, Learned, Lacked, Longed for)',
      categories: ['Liked', 'Learned', 'Lacked', 'Longed for'],
    },
    {
      id: 3,
      templateName: 'SWOT (Strengths, Weaknesses, Opportunities, Threats)',
      categories: ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
    },
  ])

  const appService = useAppService()
  const boardService = useBoardService()

  function validateNewBoardName() {
    if (!newBoardName.value.trim()) {
      newBoardNameError.value = 'This field cannot be empty!'
      return false
    }
    if (typeof newBoardName.value !== 'string') {
      return false
    }
    newBoardNameError.value = ''
    return true
  }

  function validateSelectedTemplate() {
    if (initializeWithCategories.value && selectedCategoryTemplateId.value === 0) {
      noSelectedTemplateError.value = 'You must select a template!'
      return false
    }
    noSelectedTemplateError.value = ''
    return true
  }

  function validateAll() {
    const validators = [validateNewBoardName, validateSelectedTemplate]

    for (const validator of validators) {
      if (!validator()) {
        return false
      }
    }

    return true
  }

  async function createBoard() {
    if (validateAll()) {
      const board_data = await appService.createNewBoard(newBoardName.value)
      // @ts-expect-error 'board_id' not undefined
      const board_id = board_data.board_id
      if (initializeWithCategories.value) {
        const selectedTemplate = templates.value.find(
          (template) => template.id === selectedCategoryTemplateId.value,
        )
        if (selectedTemplate) {
          for (const categoryName of selectedTemplate.categories) {
            boardService.addCategory(board_id, categoryName)
          }
        }
      }
      closeModal()
    }
  }

  function closeModal() {
    isModalOpen.value = false
    newBoardNameError.value = ''
    newBoardName.value = ''
    initializeWithCategories.value = false
    selectedCategoryTemplateId.value = 0
    noSelectedTemplateError.value = ''
  }
</script>
