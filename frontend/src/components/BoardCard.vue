<template>
  <div
    class="bg-sky-500 dark:bg-sky-900 text-sky-950 dark:text-sky-50 hover:bg-sky-600 dark:hover:bg-sky-950 transition-colors p-4 rounded-xl h-32"
  >
    {{ title }}
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  defineProps<{ title: string }>()
</script>
