<template>
  <div class="flex content-center h-12 dark:bg-slate-900 px-3 w-full" id="mainDiv">
    <filter-toggle class="flex-1" @update:selectedCategoryId="handleSelection" :categories="categories" :categoryToHighlight="selectedCategory" />
    <toggle class="flex-none content-end" label="Toggle visibility" alignment="left" v-model="visibilityChecked"/>
  </div>
  <masonry-wall :items="filteredNotes" :ssr-columns="1" :column-width="300" :gap="16" class="p-4" :class="{'blur-sm': visibilityChecked}">
    <template #default="{ item, index }">
      <div class="bg-sky-500 rounded-xl p-4">
        <span>{{ item.description }}</span>
      </div>
    </template>
  </masonry-wall>
</template>

<script setup lang="ts">
import MasonryWall from '@yeger/vue-masonry-wall'
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import FilterToggle from '@/components/FilterToggle.vue'
import Toggle from '@/components/Toggle.vue'
import { useStorage } from '@vueuse/core'

import type { Note, Category } from '@/types/InterfaceTypes.vue'

const visibilityChecked = useStorage('visibilityChecked', false)

let notes = ref<Note[]>([])
let categories = ref<Category[]>([])

onMounted(async () => {
  try {
    const { categoriesData, notesData } = await fetchNotes()
    notes.value = notesData
    categories.value = categoriesData
  } catch (err: any) {
    console.log("Error during loading data")
  } finally {
    selectedCategory.value = categories.value[0].id
  }
})

const route = useRoute()
const boardId = route.params.id as string

async function fetchNotes(): Promise<{categoriesData: Category[]; notesData: Note[]}> {
  try {
    const notes_response = await fetch('/api/notes?board_id=' + boardId)
    const cateries_response = await fetch('/api/categories?board_id=' + boardId)

    if (!notes_response.ok) {
      const resp = await notes_response.text()
      console.error('Error response:', resp)
      throw new Error('Network response was not ok: ' + notes_response.statusText)
    }

    if (!cateries_response.ok) {
      const resp = await cateries_response.text()
      console.error('Error response:', resp)
      throw new Error('Network response was not ok: ' + cateries_response.statusText)
    }

    const categoriesData = (await cateries_response.json()) as Category[]
    const notesData = (await notes_response.json()) as Note[]
    return { categoriesData, notesData }
  } catch (err) {
    console.error('Error fetching notes:', err)
    throw new Error("Failed to fetch categories and notes.")
  }
}

const selectedCategory = ref<number | null>(null)
const filteredNotes = computed(() => {
  if (selectedCategory.value === null)
    return notes.value.filter((n) => n.category === categories.value[0].id)

  return notes.value.filter((n) => n.category === selectedCategory.value)
})

function handleSelection(index: number) {
  console.log('Selected:', index)
  selectedCategory.value = index
}
</script>
