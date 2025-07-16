<template>
  <div
    class="bg-sky-500 text-sky-950 hover:bg-sky-700 dark:bg-slate-600 dark:text-slate-50 dark:hover:bg-slate-500 transition-colors p-4 rounded-xl h-32"
  >
    {{ title }}
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  defineProps<{ title: string }>()
</script>
