<template>
  <button
    type="button"
    class="transition-colors inline-flex items-center gap-x-2 rounded-sm text-sm font-semibold cursor-pointer"
    :class="`${colors} ${spacing}`"
  >
    <slot>
      {{ props.label }}
    </slot>
  </button>
</template>

<script setup lang="ts">
  import { computed, defineProps } from 'vue'

  const props = defineProps<{
    label?: string
    variant?: 'primary' | 'outline' | 'danger' | 'icon' | 'icon_danger'
  }>()

  const colors = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'button-color-primary text-color-over-primary'
    case 'outline':
      return 'background-color-bold text-color border border-color border-color-hover'
    case 'danger':
      return 'button-color-danger text-color-over-primary'
    case 'icon':
      return 'text-color text-hover-color-primary'
    case 'icon_danger':
      return 'text-color-danger'
    default:
      return 'button-color text-color' // fallback if no variant is given
  }
})

  const spacing = computed(() => {
    if (props.variant === "icon" || props.variant === "icon_danger") {
      return 'px-2 py-1'
    } else {
      return 'px-3 py-2'
    }
  })
</script>
