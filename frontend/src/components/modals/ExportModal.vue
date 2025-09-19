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
      @close="closeExportModal()"
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
                        d="M19 10V4a1 1 0 0 0-1-1H9.914a1 1 0 0 0-.707.293L5.293 7.207A1 1 0 0 0 5 7.914V20a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2M10 3v4a1 1 0 0 1-1 1H5m5 6h9m0 0-2-2m2 2-2 2"
                      />
                    </svg>
                  </div>
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <DialogTitle
                      as="h3"
                      class="text-color text-xl font-medium font-semibold"
                    >
                      Export Board
                    </DialogTitle>
                    <div class="mt-2">
                      <label
                        for="export_content"
                        class="block mb-2 text-sm font-medium text-color"
                      >
                        Board Content
                      </label>
                      <textarea
                        id="export_content"
                        v-model="exportContent"
                        class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
                        rows="10"
                        cols="50"
                        disabled
                      />
                      <ButtonInputComponent
                        class="w-full justify-center mt-2 sm:w-auto"
                        @click="exportJSON()"
                        label="Export as JSON"
                        variant="outline"
                      />
                      <ButtonInputComponent
                        class="w-full justify-center mt-2 sm:w-auto sm:ml-3"
                        @click="exportMarkdown()"
                        label="Export as Markdown"
                        variant="outline"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div class="background-color px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <ButtonInputComponent
                  class="w-full justify-center mt-3 sm:mt-0 sm:w-auto"
                  @click="closeExportModal()"
                  label="Close"
                  variant="primary"
                />
                <ButtonInputComponent
                  v-if="isSupported"
                  class="w-full justify-center mt-3 sm:mt-0 sm:w-auto mr-2"
                  @click="copy(exportContent)"
                  :variant="copied ? 'outline_success' : 'outline'"
                >
                  <svg
                    v-if="!copied"
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
                      d="M15 4h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3m0 3h6m-6 5h6m-6 4h6M10 3v4h4V3h-4Z"
                    />
                  </svg>
                  <svg
                    v-else
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
                      d="M15 4h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3m0 3h6m-6 7 2 2 4-4m-5-9v4h4V3h-4Z"
                    />
                  </svg>
                </ButtonInputComponent>
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
  import { useClipboard } from '@vueuse/core'
  import ButtonInputComponent from '@/components/input/ButtonInputComponent.vue'
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'

  const exportContent = ref('')

  const isModalOpen = defineModel<boolean>('isModalOpen')

  const props = defineProps(['currentBoardId'])

  const boardService = useBoardService()

  const { text, copy, copied, isSupported } = useClipboard({ exportContent })

  async function exportJSON() {
    exportContent.value = await boardService.exportJson(props.currentBoardId)
  }

  async function exportMarkdown() {
    exportContent.value = await boardService.exportMarkdown(props.currentBoardId)
  }

  function closeExportModal() {
    isModalOpen.value = false
  }
</script>
