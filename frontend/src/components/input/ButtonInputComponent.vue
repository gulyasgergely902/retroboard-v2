<template>
  <button
    type="button"
    class="transition-colors inline-flex items-center gap-x-2 rounded-sm text-sm font-semibold cursor-pointer"
    :class="[colors, spacing]"
  >
    <slot>
      {{ props.label }}
    </slot>
  </button>
</template>

<script setup lang="ts">
  import { computed, defineProps } from 'vue'

  const error = defineModel<boolean>('error')

  const props = defineProps<{
    label?: string
    primary?: boolean
    outline?: boolean
    dashed_outline?: boolean
    danger?: boolean
    icon?: boolean
    icon_danger?: boolean
  }>()

  const colors = computed(() => {
    if (props.primary) {
      return 'button-color-primary text-color-over-primary'
    } else if (props.outline) {
      return 'background-color-bold text-color border border-color border-color-hover'
    } else if (props.dashed_outline) {
      return error.value
        ? 'background-color-bold text-color input-error'
        : 'background-color-bold text-color border border-dashed border-color border-color-hover'
    } else if (props.danger) {
      return 'button-color-danger text-color-over-primary'
    } else if (props.icon) {
      return 'text-color text-hover-color-primary'
    } else if (props.icon_danger) {
      return 'text-color-danger'
    }
    return 'button-color text-color'
  })

  const spacing = computed(() => {
    if (props.icon || props.icon_danger) {
      return 'px-2 py-1'
    } else {
      return 'px-3 py-2'
    }
  })
</script>
