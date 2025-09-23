<template>
  <div class="flex items-center gap-2 mt-2">
    <KeyboardKey :char="char" variant="normal"/>
    <span class="description text-sm font-medium text-color">{{ description }}</span>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  import KeyboardKey from '@/components/KeyboardKey.vue'

  defineProps<{
    char: string
    description: string
  }>()
</script>

<style scoped>
</style>
