<template>
  <div class="background-color-bold pt-4 rounded-lg w-full">
    <div class="flex content-center h-8 px-4 w-full">
      <span class="text-color ms-1 text-xl font-medium">Active Boards</span>
      <button
        type="button"
        @click="isModalOpen = true"
        class="background-color-primary text-color-over-primary transition-colors ml-auto inline-flex items-center gap-x-2 rounded-sm px-3 py-2 text-sm font-semibold cursor-pointer"
      >
        Create Board
      </button>
      <NewBoardModal v-model:is-modal-open="isModalOpen" />
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 p-2">
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
        <BoardCard
          v-if="board.id"
          :title="board.name"
        />
        <BoardCard
          v-else
          class="grayscale"
          title="Board data is missing"
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
