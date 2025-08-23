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
  <SettingsModal v-model:is-settings-modal-open="isSettingsModalOpen"/>
  <nav>
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <RouterLink
        to="/"
        class="flex items-center space-x-3 rtl:space-x-reverse"
      >
        <span class="text-color self-center text-2xl font-semibold whitespace-nowrap">
          RetroBoard
        </span>
      </RouterLink>
      <Menu
        as="div"
        class="relative ml-3"
      >
        <MenuButton
          class="relative flex rounded-full cursor-pointer"
        >
          <span class="absolute -inset-1.5" />
          <span class="sr-only">Open user menu</span>
          <svg
            class="w-6 h-6 text-gray-800 dark:text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-width="2"
              d="M5 7h14M5 12h14M5 17h14"
            />
          </svg>
        </MenuButton>

        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <MenuItems
            class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md background-color py-1 border-1 border-color"
          >
            <MenuItem>
              <a
                href="#"
                class="button-color text-color block px-4 py-2 text-sm"
                @click="isSettingsModalOpen = true"
              >
                Settings
              </a>
            </MenuItem>
          </MenuItems>
        </transition>
      </Menu>
    </div>
  </nav>
  <div
    v-if="appService.getSettingValue('notification_banner_text')"
    class="w-full background-color-alert rounded-sm"
  >
    <p class="text-color-alert p-2">{{ appService.getSettingValue('notification_banner_text') }}</p>
  </div>
</template>

<script setup lang="ts">
  import { RouterLink } from 'vue-router'
  import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
  import SettingsModal from './SettingsModal.vue'
  import { useAppService } from '@/services/app/app.service'

  import { ref } from 'vue'

  const appService = useAppService()

  const isSettingsModalOpen = ref(false)
</script>
