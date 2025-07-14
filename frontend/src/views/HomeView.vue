<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
    <BoardCard
      v-if="appService.loading"
      v-for="n in 10"
      class="blur-sm grayscale brightness-150"
      title="Boards are loading..."
    />
    <RouterLink
      v-else
      v-for="board in appService.boards"
      :to="{ name: 'board', params: { id: String(board.id) } }"
    >
      <BoardCard v-if="board.id" :title="board.name" />
      <BoardCard v-else class="grayscale" title="Board data is missing" />
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { useAppService } from '@/services/app/app.service'
import BoardCard from '@/components/BoardCard.vue'

const appService = useAppService()

void appService.fetchBoards()
</script>
