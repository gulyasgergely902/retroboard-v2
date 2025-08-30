<template>
  <Menu as="div" class="relative inline-block">
    <MenuButton>
      <ButtonInputComponent
        :label="buttonLabel"
        v-model:error="error"
        dashed_outline
        icon
      />
    </MenuButton>
    <MenuItems
      as="div"
      class="absolute bottom-full left-0 mb-2 background-color text-color border border-color rounded-md w-full sm:w-50 max-h-30 overflow-x-hidden overflow-y-auto"
    >
      <MenuItem
        as="div"
        class=""
        v-for="option in props.options"
        :key="option.id"
      >
        <div
          id="category_list"
          class="w-full flex items-center justify-between button-color px-2 py-2 rounded-sm cursor-pointer"
          @click="setSelection(option)"
        >
          <span class="text-color text-sm">{{ option.name }}</span>
        </div>
      </MenuItem>
    </MenuItems>
  </Menu>
</template>

<script setup lang="ts">
  import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
  import { defineProps, ref } from 'vue'
  import ButtonInputComponent from './ButtonInputComponent.vue'

  import type { Category } from '@/services/board/types'

  const selection = defineModel<number>('selection')
  const error = defineModel<boolean>('error')

  const buttonLabel = ref('Category')

  const props = defineProps<{
    label: string
    options: Category[]
  }>()

  function setSelection(category: Category) {
    selection.value = category.id
    buttonLabel.value = category.name
  }
</script>
