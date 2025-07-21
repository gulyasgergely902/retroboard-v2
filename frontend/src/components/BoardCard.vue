<template>
  <div
    class="background-color text-color transition-colors p-4 rounded-md h-32"
  >
    {{ title }}
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  defineProps<{ title: string }>()
</script>
