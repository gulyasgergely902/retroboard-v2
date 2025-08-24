<template>
  <div class="flex mt-4">
    <div class="flex items-center h-5">
      <input
        id="helper-checkbox"
        aria-describedby="helper-checkbox-text"
        type="checkbox"
        value=""
        v-model="checkedState"
        class="w-4 h-4 text-color background-color border-gray-300 rounded-sm dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
      />
    </div>
    <div class="ms-2 text-sm">
      <label
        for="helper-checkbox"
        class="font-medium text-color"
      >
        {{ props.label }}
      </label>
      <p
        v-if="props.description"
        id="helper-checkbox-text"
        class="text-xs font-normal text-color-muted mt-1"
      >
        {{ description }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'

  const checkedState = defineModel<boolean>('checkedState')

  const props = defineProps(['label', 'description'])
</script>
