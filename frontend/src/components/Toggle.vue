<template>
  <label class="inline-flex items-center cursor-pointer mr-2 ml-4">
    <!-- prettier-ignore -->
    <span
      v-if="alignment === 'left'"
      class="me-3 text-sm font-medium text-color"
    >{{ label }}</span>
    <input
      type="checkbox"
      value=""
      v-model="checked"
      class="sr-only peer"
    />
    <div
      class="relative w-11 h-6 bg-blue-200 hover:bg-blue-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-blue-950 dark:hover:bg-blue-300 transition-colors peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:dark:bg-slate-900 after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500 dark:peer-checked:bg-blue-400"
    ></div>
    <!-- prettier-ignore -->
    <span
      v-if="alignment === 'right'"
      class="ms-3 mr-1 text-sm font-medium text-color"
    >{{ label }}</span>
  </label>
</template>

<script setup lang="ts">
  import { computed } from 'vue'

  const props = defineProps<{ label: string; alignment: string; modelValue: boolean }>()
  const emit = defineEmits<(event: 'update:modelValue', value: boolean) => void>()

  const checked = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value),
  })
</script>
