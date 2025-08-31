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
  <NewBoardModal v-model:is-modal-open="isModalOpen" />
  <div class="background-color-bold pt-4 rounded-lg w-full">
    <div class="flex content-center h-8 px-2 w-full">
      <span class="text-color ms-1 text-xl font-medium">Active Boards</span>
      <ButtonInputComponent
        class="ml-auto"
        @click="isModalOpen = true"
        label="Create Board"
        variant="primary"
      />
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
  import NewBoardModal from '@/components/modals/NewBoardModal.vue'
  import ButtonInputComponent from '@/components/input/ButtonInputComponent.vue'

  const isModalOpen = ref(false)

  const appService = useAppService()

  void appService.fetchBoards()
</script>
