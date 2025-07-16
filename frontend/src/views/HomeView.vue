<template>
  <div class="flex content-center h-8 px-3 w-full">
    <span class="text-gray-950 dark:text-slate-50 ms-1 text-xl font-medium">Active Boards</span>
    <button
      type="button"
      @click="isModalOpen = true"
      class="bg-sky-500 dark:bg-sky-900 text-sky-950 dark:text-sky-50 hover:bg-sky-600 dark:hover:bg-sky-950 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300 ml-auto inline-flex items-center gap-x-2 rounded-lg px-4 py-2 text-sm font-semibold"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-5"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 4.5v15m7.5-7.5h-15"
        />
      </svg>

      Create Board
    </button>
    <NewBoardModal v-model:is-modal-open="isModalOpen"/>
  </div>
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
</template>

<script setup lang="ts">
  import { useAppService } from '@/services/app/app.service'
  import BoardCard from '@/components/BoardCard.vue'

  const appService = useAppService()

  void appService.fetchBoards()
</script>
