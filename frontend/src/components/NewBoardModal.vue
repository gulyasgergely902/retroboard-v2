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
              <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
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
                        d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z"
                      />
                    </svg>
                  </div>
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <DialogTitle
                      as="h3"
                      class="text-base font-semibold text-gray-900"
                    >
                      Create Board
                    </DialogTitle>
                    <div class="mt-2">
                      <label
                        for="board_name"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                      >
                        Board Name
                      </label>
                      <input
                        type="text"
                        id="board_name"
                        v-model="newBoardName"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-sky-500 focus:border-sky-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-sky-500 dark:focus:border-sky-500"
                        placeholder="My Board"
                        required
                      />
                      <p
                        v-if="newBoardNameError"
                        class="text-red-500 text-sm"
                      >
                        Board name cannot be empty!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-white px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button
                  type="button"
                  class="bg-sky-500 dark:bg-slate-600 text-sky-950 hover:bg-sky-600 dark:text-sky-50 dark:hover:bg-slate-500 hover:text-slate-950 dark:hover:text-sky-50 transition-colors inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold sm:ml-3 sm:w-auto"
                  @click="createBoard()"
                >
                  Create
                </button>
                <button
                  type="button"
                  class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs ring-1 ring-gray-300 ring-inset hover:bg-gray-50 sm:mt-0 sm:w-auto"
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
  import { useAppService } from '@/services/app/app.service'
  const newBoardNameError = ref(false)
  const isModalOpen = defineModel<boolean>('isModalOpen')
  const newBoardName = defineModel<string>('newBoardName')
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
  } from '@headlessui/vue'

  const appService = useAppService()

  const validateNewBoardName = () => {
    if (!newBoardName.value?.trim()) {
      newBoardNameError.value = true
      return false
    }
    newBoardNameError.value = false
    return true
  }

  function createBoard() {
    if (validateNewBoardName() && typeof newBoardName.value === 'string') {
      appService.createNewBoard(newBoardName.value)
      newBoardName.value = ''
      isModalOpen.value = false
    }
  }
</script>
