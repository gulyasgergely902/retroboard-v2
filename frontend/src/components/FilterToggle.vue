<template>
  <div class="inline-flex items-center mr-2 w-1/2">
    <span class="text-color me-3 text-sm font-medium">Filters</span>
    <div
      class="overflow-x-auto overflow-y-hidden whitespace-nowrap fade-right no-scrollbar flex items-center mx-auto px-4"
    >
      <button
        type="button"
        @click="selectOption(-1)"
        :class="[
          categoryToHighlight === -1
            ? 'button-color-primary text-color-over-primary'
            : 'button-color-primary-soft text-color',
        ]"
        class="px-4 py-2 text-sm font-medium rounded-sm focus:z-10 mx-1 transition-colors cursor-pointer"
      >
        All
      </button>
      <div class="inline-block mx-2 self-stretch vertical-separator separator-width"></div>
      <button
        v-for="category in categories"
        :key="category.id"
        type="button"
        @click="selectOption(category.id)"
        :class="[
          categoryToHighlight === category.id
            ? 'button-color-primary text-color-over-primary'
            : 'button-color-primary-soft text-color',
        ]"
        class="px-4 py-2 text-sm font-medium rounded-sm focus:z-10 mx-1 transition-colors cursor-pointer"
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
