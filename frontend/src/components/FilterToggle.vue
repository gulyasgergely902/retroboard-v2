<template>
  <div class="inline-flex items-center mr-2 ml-1 w-3/4" id="innerDiv">
    <span class="me-3 text-sm font-medium text-gray-900 dark:text-gray-300">Filters</span>
    <div class="overflow-x-auto overflow-y-hidden whitespace-nowrap h-12 fade-right no-scrollbar">
      <button
        v-for="category in categories"
        type="button"
        @click="selectOption(category.id)"
        :class="[categoryToHighlight === category.id ? 'bg-sky-500' : 'bg-sky-100']"
        class="px-4 py-2 text-sm font-medium text-slate-950 bg-sky-100 rounded-xl hover:bg-sky-300 hover:text-slate-950 focus:z-10 focus:ring-2 focus:ring-sky-700 focus:text-sky-700 dark:bg-slate-800 dark:text-sky-50 dark:hover:text-sky-50 dark:hover:bg-sky-700 dark:focus:ring-sky-500 dark:focus:text-white m-1 cursor-pointer"
      >
        {{ category.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
defineProps(['categories', 'categoryToHighlight'])

const emit = defineEmits<{
  (e: 'update:categoryToHighlight', index: number): void
}>()

const selectOption = (index: number) => {
  emit('update:categoryToHighlight', index)
}
</script>
<style lang="css" scoped>
.fade-right {
  background-color: white; /* or whatever background you want */
  width: 100%;

  /* Apply a mask to fade out on the right */
  -webkit-mask-image: linear-gradient(to right, black 95%, transparent 98%);
  mask-image: linear-gradient(to right, black 95%, transparent 98%);
}
</style>
