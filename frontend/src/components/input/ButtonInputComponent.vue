<template>
  <button
    type="button"
    class="transition-colors inline-flex items-center gap-x-2 rounded-sm px-3 py-2 text-sm font-semibold cursor-pointer"
    :class="`${classes}`"
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
    primary?: boolean
    outline?: boolean
    danger?: boolean
    icon?: boolean
    icon_danger?: boolean
  }>()

  const classes = computed(() => {
    if (props.primary) {
      return 'button-color-primary text-color-over-primary'
    } else if (props.outline) {
      return 'background-color text-color border border-color border-color-hover'
    } else if (props.danger) {
      return 'button-color-danger text-color-over-primary'
    } else if (props.icon) {
        return 'text-color text-hover-color-primary'
    } else if (props.icon_danger) {
        return 'text-color-danger'
    }
    return 'button-color text-color'
  })
</script>
