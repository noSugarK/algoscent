<template>
  <div class="mb-8">
    <div class="flex justify-between text-sm text-gray-500 mb-2">
      <span>第 {{ current }} 题</span>
      <span>共 {{ total }} 题</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div
        class="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-500"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: Number,
  total: Number
})

const percentage = computed(() => Math.round((props.current / props.total) * 100))
</script>