<template>
  <div
    class="text-color transition-colors p-4 rounded-md border-1 border-color h-32"
    :class="[dummy ? 'background-color-dummy' : 'background-color']"
  >
    <p
      v-if="!dummy"
      class="text-color text-lg"
    >
      {{ title }}
    </p>
    <p
      v-if="!dummy"
      class="background-color-primary text-color-over-primary text-xs inline-block max-w-max rounded-full py-1 px-2 mt-2"
    >
      Notes: {{ noteCount }}
    </p>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  withDefaults(
    defineProps<{
      title?: string
      noteCount?: number
      dummy?: boolean
    }>(),
    {
      dummy: false,
    },
  )
</script>
