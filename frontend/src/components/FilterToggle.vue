<template>
  <div
    class="inline-flex items-center mr-2 ml-1 w-3/4"
    id="innerDiv"
  >
    <span class="text-sky-950 dark:text-sky-50 me-3 text-sm font-medium">Filters</span>
    <div class="overflow-x-auto overflow-y-hidden whitespace-nowrap h-12 fade-right no-scrollbar">
      <button
        v-for="category in categories"
        type="button"
        @click="selectOption(category.id)"
        :class="[categoryToHighlight === category.id ? 'bg-sky-500 dark:bg-sky-900' : 'bg-sky-100 hover:bg-sky-300 dark:bg-sky-950 dark:hover:bg-sky-900']"
        class="text-sky-950 dark:text-sky-50 px-4 py-2 text-sm font-medium rounded-xl focus:z-10 focus:ring-2 focus:ring-sky-700 focus:text-sky-700 dark:focus:ring-sky-500 dark:focus:text-white m-1 transition-colors cursor-pointer"
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
    width: 100%;

    /* Apply a mask to fade out on the right */
    -webkit-mask-image: linear-gradient(to right, black 95%, transparent 98%);
    mask-image: linear-gradient(to right, black 95%, transparent 98%);
  }
  .fade-right-dark {
    width: 100%;

    /* Apply a mask to fade out on the right */
    -webkit-mask-image: linear-gradient(to right, black 95%, transparent 98%);
    mask-image: linear-gradient(to right, black 95%, transparent 98%);
  }
</style>
