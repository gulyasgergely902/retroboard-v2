<template>
  <div class="flex content-center h-12 dark:bg-slate-900 px-3 w-full" id="mainDiv">
    <FilterToggle
      class="flex-1"
      :categories="boardService.categories"
      v-model:categoryToHighlight="boardService.selectedCategory"
    />
    <Toggle
      class="flex-none content-end"
      label="Toggle visibility"
      alignment="left"
      v-model="visibilityChecked"
    />
  </div>
  <MasonryWall
    :items="boardService.filteredNotes"
    :ssr-columns="1"
    :column-width="300"
    :gap="16"
    class="p-4"
    :class="{ 'blur-sm': visibilityChecked }"
  >
    <template #default="{ item }">
      <div class="bg-sky-500 rounded-xl p-4">
        <span>{{ item.description }}</span>
      </div>
    </template>
  </MasonryWall>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useLocalStorage } from '@vueuse/core'
import { useBoardService } from '@/services/board/board.service'
import MasonryWall from '@yeger/vue-masonry-wall'
import FilterToggle from '@/components/FilterToggle.vue'
import Toggle from '@/components/Toggle.vue'

const route = useRoute()
const boardService = useBoardService()
const visibilityChecked = useLocalStorage('visibilityChecked', false)

void boardService.fetchBoardData(route.params.id as string)
</script>
