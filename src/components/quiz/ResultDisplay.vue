<template>
  <div class="bg-white rounded-3xl p-8 shadow-xl max-w-3xl mx-auto border border-gray-100">
    <div class="text-center mb-8">
      <div class="w-20 h-20 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h2 class="text-3xl font-bold text-gray-800 mb-2">🎉 专属香氛报告</h2>
      <p class="text-gray-600">基于你的选择，我们为你推荐最适合的疗愈香氛</p>
    </div>

    <div class="bg-gray-50 rounded-2xl p-6 mb-6">
      <h3 class="font-semibold text-lg mb-3 text-gray-800">📊 你的答题数据</h3>
      <pre class="text-xs text-gray-700 bg-white p-4 rounded-lg overflow-auto max-h-60">{{ formattedReport }}</pre>
    </div>

    <div class="flex flex-col sm:flex-row gap-4">
      <button
        @click="onRestart"
        class="flex-1 px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-xl transition-colors"
      >
        🔄 重新测试
      </button>
      <button
        @click="onSubmit"
        class="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white font-medium rounded-xl transition-all transform hover:scale-105"
      >
        💾 提交报告
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  report: Object
})

const emit = defineEmits(['restart', 'submit'])

const onRestart = () => emit('restart')
const onSubmit = () => emit('submit')

const formattedReport = computed(() => {
  return JSON.stringify(props.report, null, 2)
})
</script>