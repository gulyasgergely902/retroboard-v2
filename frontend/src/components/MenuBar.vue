<template>
  <nav class="bg-white border-gray-200 dark:bg-slate-900">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <RouterLink
        to="/"
        class="flex items-center space-x-3 rtl:space-x-reverse"
      >
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-slate-50">
          RetroBoard
        </span>
      </RouterLink>
      <button
        type="button"
        class="bg-sky-500 hover:bg-sky-300 dark:bg-slate-600 dark:hover:bg-slate-500 dark:text-slate-50 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300 ml-auto inline-flex items-center gap-x-2 rounded-lg px-4 py-2 text-sm font-semibold shadow-sm"
      >
        <!-- Plus icon: Heroicons mini/solid “plus” (20×20) -->
        <svg
          class="h-5 w-5"
          fill="currentColor"
          viewBox="0 0 20 20"
          aria-hidden="true"
        >
          <path
            fill-rule="evenodd"
            d="M10 5a.75.75 0 01.75.75v3.5h3.5a.75.75 0 010 1.5h-3.5v3.5a.75.75 0 01-1.5 0v-3.5h-3.5a.75.75 0 010-1.5h3.5v-3.5A.75.75 0 0110 5z"
            clip-rule="evenodd"
          />
        </svg>
        Add item
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
  import { RouterLink } from 'vue-router'
</script>
