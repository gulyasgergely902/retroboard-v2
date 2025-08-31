<!--
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<template>
  <div class="inline-flex items-center mr-2 w-full">
    <span class="text-color me-3 text-sm font-medium">Filters</span>
    <div
      class="overflow-x-auto overflow-y-hidden whitespace-nowrap fade-right no-scrollbar flex items-center px-4"
    >
      <ButtonInputComponent
        label="All"
        @click="selectOption(-1)"
        class="px-4 py-2 text-sm font-medium rounded-sm focus:z-10 mx-1 transition-colors cursor-pointer"
        :variant="categoryToHighlight === -1 ? 'primary' : 'primary_soft'"
      />
      <div class="inline-block mx-2 self-stretch vertical-separator separator-width"></div>
      <ButtonInputComponent
        v-for="category in categories"
        :key="category.id"
        @click="selectOption(category.id)"
        :label="category.name"
        class="px-4 py-2 text-sm font-medium rounded-sm focus:z-10 mx-1 transition-colors cursor-pointer"
        :variant="categoryToHighlight === category.id ? 'primary' : 'primary_soft'"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  import ButtonInputComponent from '@/components/input/ButtonInputComponent.vue'

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
    -webkit-mask-image: linear-gradient(to right, black 95%, transparent 98%);
    mask-image: linear-gradient(to right, black 95%, transparent 98%);
  }
</style>
