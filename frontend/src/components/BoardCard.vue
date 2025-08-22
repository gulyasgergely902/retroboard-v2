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
  <div
    class="text-color transition-colors p-4 rounded-md border-1 border-color border-color-hover h-32"
    :class="[dummy ? 'background-color-dummy' : 'background-color']"
  >
    <p
      v-if="!dummy"
      class="text-color text-lg"
    >
      {{ title }}
    </p>
    <p
      v-if="!dummy"
      class="background-color-primary text-color-over-primary text-xs inline-block max-w-max rounded-full py-1 px-2 mt-2"
    >
      Notes: {{ noteCount }}
    </p>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'
  withDefaults(
    defineProps<{
      title?: string
      noteCount?: number
      dummy?: boolean
    }>(),
    {
      dummy: false,
    },
  )
</script>
