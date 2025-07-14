<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
    <BoardCard
      v-if="loading"
      v-for="n in 10"
      class="blur-sm grayscale brightness-150"
      title="Boards are loading..."
    />
    <RouterLink
      v-else
      v-for="board in boards"
      :to="{ name: 'board', params: { id: String(board.id) } }"
    >
      <BoardCard v-if="board.id" :title="board.name" />
      <BoardCard v-else class="grayscale" title="Board data is missing" />
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import type { Board } from '@/types/app'
import { ref } from 'vue'
import { $fetch } from '@/composables/fetch'
import BoardCard from '@/components/BoardCard.vue'

const loading = ref(true)
const boards = ref<Board[]>([])

void fetchBoards()

async function fetchBoards() {
  try {
    loading.value = true

    const response = await $fetch<Board[]>('/api/boards')
    boards.value = await response.json()
  } catch (err) {
    console.error('Error fetching boards:', err)
  } finally {
    loading.value = false
  }
}
</script>
