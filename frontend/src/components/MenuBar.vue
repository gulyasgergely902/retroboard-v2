<template>
  <nav>
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <RouterLink
        to="/"
        class="flex items-center space-x-3 rtl:space-x-reverse"
      >
        <span class="text-color self-center text-2xl font-semibold whitespace-nowrap">
          RetroBoard
        </span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
  import { RouterLink } from 'vue-router'
</script>
