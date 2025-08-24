<template>
  <div class="mt-2 mb-1">
    <label
      for="select-input"
      class="block mt-4 mb-2 text-sm font-medium text-color"
    >
      {{ props.label }}
    </label>
    <select
      id="select-input"
      v-model="selection"
      class="background-color-bold text-color text-sm rounded-sm block w-full p-2.5"
      :class="{ 'input-error': error }"
    >
      <option
        v-for="item in options"
        :key="item.id"
        :value="item.id"
      >
        {{ item.name }}
      </option>
    </select>
    <label
      v-if="props.description"
      for="select-input"
      class="block mt-2 mb-2 text-xs font-medium text-color-muted"
    >
      {{ props.description }}
    </label>
    <label
      v-if="error"
      for="select-input"
      class="block mt-2 mb-2 text-xs font-medium text-color-danger"
    >
      {{ error }}
    </label>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'

  const selection = defineModel<number>('selection')
  const error = defineModel<string>('error')

  const props = defineProps(['label', 'description', 'options'])
</script>
