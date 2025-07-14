<template>
  <div class="flex content-center h-12 dark:bg-slate-900 px-3 w-full" id="mainDiv">
    <FilterToggle
      class="flex-1"
      :categories="categories"
      v-model:categoryToHighlight="selectedCategory"
    />
    <Toggle
      class="flex-none content-end"
      label="Toggle visibility"
      alignment="left"
      v-model="visibilityChecked"
    />
  </div>
  <MasonryWall
    :items="filteredNotes"
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
import type { Note, Category } from '@/types/app'
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useLocalStorage } from '@vueuse/core'
import { $fetch } from '@/composables/fetch'
import MasonryWall from '@yeger/vue-masonry-wall'
import FilterToggle from '@/components/FilterToggle.vue'
import Toggle from '@/components/Toggle.vue'

const route = useRoute()
const boardId = route.params.id as string

const visibilityChecked = useLocalStorage('visibilityChecked', false)
const notes = ref<Note[]>([])
const categories = ref<Category[]>([])
const selectedCategory = ref<number | null>(null)
const filteredNotes = computed(() =>
  notes.value.filter((n) => n.category === selectedCategory.value),
)

void fetchNotes()

async function fetchNotes() {
  try {
    const [notes_response, categories_response] = await Promise.all([
      $fetch<Note[]>(`/api/notes?board_id=${boardId}`),
      $fetch<Category[]>(`/api/categories?board_id=${boardId}`),
    ])

    categories.value = await categories_response.json()
    notes.value = await notes_response.json()
  } catch (err) {
    console.error('Error fetching notes:', err)
  } finally {
    if (categories.value.length > 0) {
      selectedCategory.value = categories.value[0].id
    }
  }
}
</script>
