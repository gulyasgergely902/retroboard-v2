<template>
  <NewBoardModal v-model:is-modal-open="isModalOpen" />
  <div class="background-color-bold pt-4 rounded-lg w-full">
    <div class="flex content-center h-8 px-2 w-full">
      <span class="text-color ms-1 text-xl font-medium">Active Boards</span>
      <button
        type="button"
        @click="isModalOpen = true"
        class="background-color-primary text-color-over-primary transition-colors ml-auto inline-flex items-center gap-x-2 rounded-sm px-3 py-2 text-sm font-semibold cursor-pointer"
      >
        Create Board
      </button>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 p-2">
      <!-- eslint-disable -->
      <BoardCard
        v-if="appService.loading"
        v-for="n in 10"
        :key="n"
        class="grayscale animate-pulse"
        :dummy="true"
      />
      <RouterLink
        v-else
        v-for="board in appService.boards"
        :key="board.id"
        :to="{ name: 'board', params: { id: String(board.id) } }"
      >
        <BoardCard
          :title="board.name"
          :note-count="board.note_count"
        />
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useAppService } from '@/services/app/app.service'
  import { ref } from 'vue'
  import BoardCard from '@/components/BoardCard.vue'
  import NewBoardModal from '@/components/NewBoardModal.vue'

  const isModalOpen = ref(false)

  const appService = useAppService()

  void appService.fetchBoards()
</script>
