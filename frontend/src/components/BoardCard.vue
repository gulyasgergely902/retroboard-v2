<template>
  <div
    class="background-color text-color transition-colors p-4 rounded-md border-1 border-color h-32"
  >
    <p class="text-color text-lg">{{ title }}</p>
    <p
      class="background-color-primary text-color-over-primary text-xs inline-block rounded-full py-1 px-2 mt-2"
    >
      Notes: {{ noteCount }}
    </p>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  defineProps<{ title: string; noteCount: number }>()
</script>
