<template>
  <div
    class="background-color-bold text-color inline-flex items-center justify-center border-2 border-solid border-color-key rounded-md font-mono font-semibold"
    :class="size"
  >
    {{ char }}
  </div>
</template>

<script setup lang="ts">
  import { computed, defineProps } from 'vue'

  const props = defineProps<{
    char: string
    variant?: 'normal' | 'small'
  }>()

  const size = computed(() => {
    switch (props.variant) {
      case 'normal':
        return 'w-8 h-6 text-sm'
      case 'small':
        return 'min-w-4 w-auto h-4 text-xs opacity-50'
      default:
        return 'min-w-6 w-auto h-6 text-sm'
    }
  })
</script>