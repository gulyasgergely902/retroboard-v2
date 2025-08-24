<template>
  <div class="mt-2 mb-1">
    <label
      for="text-input"
      class="block mb-2 text-sm font-medium text-color"
    >
      {{ props.label }}
    </label>
    <input
      type="text"
      id="text-input"
      v-model="textContent"
      class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
      :class="{ 'input-error': error }"
    />
    <label
      v-if="props.description"
      for="text-input"
      class="block mt-2 mb-2 text-xs font-medium text-color-muted"
    >
      {{ props.description }}
    </label>
    <label
      v-if="error"
      for="text-input"
      class="block mt-2 mb-2 text-xs font-medium text-color-danger"
    >
      {{ error }}
    </label>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'

  const textContent = defineModel<string>('textContent')
  const error = defineModel<string>('error')

  const props = defineProps(['label', 'description'])
</script>
