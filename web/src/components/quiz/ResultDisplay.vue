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
      
      <!-- 测验基本信息 -->
      <div class="mt-4 flex flex-wrap justify-center gap-4 text-sm text-gray-600">
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>用时: {{ durationDisplay }}</span>
        </div>
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ props.report.completedAt }}</span>
        </div>
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>题号: {{ props.report.id }}</span>
        </div>
      </div>
    </div>

    <!-- 答题数据分析 -->
    <div class="bg-gray-50 rounded-2xl p-6 mb-6">
      <h3 class="font-semibold text-lg mb-3 text-gray-800">📊 你的答题分析</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <h4 class="font-medium text-gray-700 mb-2">回答题目数量</h4>
          <div class="text-3xl font-bold text-indigo-500">{{ totalQuestions }}</div>
        </div>
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <h4 class="font-medium text-gray-700 mb-2">平均每题用时</h4>
          <div class="text-3xl font-bold text-purple-500">{{ avgTimePerQuestion }}</div>
        </div>
      </div>
      
      <!-- 答题详情（可折叠） -->
      <div class="mt-4">
        <button 
          @click="showDetails = !showDetails"
          class="flex items-center text-sm text-indigo-600 hover:text-indigo-800"
        >
          <span>{{ showDetails ? '隐藏' : '查看' }}详细答题记录</span>
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-4 w-4 ml-1 transform transition-transform" 
            :class="{ 'rotate-180': showDetails }"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        
        <div v-if="showDetails" class="mt-2 bg-white p-4 rounded-lg shadow-sm overflow-auto max-h-60">
          <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ formattedReport }}</pre>
        </div>
      </div>
    </div>

    <div class="flex flex-col sm:flex-row gap-4">
      <button
        @click="onRestart"
        class="flex-1 px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-xl transition-colors"
      >
        🔄 重新测试
      </button>
      <button
        @click="onHistory"
        class="flex-1 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-xl transition-colors"
      >
        📋 查看历史记录
      </button>
      <button
        @click="onSubmit"
        class="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white font-medium rounded-xl transition-all transform hover:scale-105"
      >
        💾 保存报告
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  report: Object
})

const emit = defineEmits(['restart', 'submit'])
const router = useRouter()
const showDetails = ref(false)

const onRestart = () => emit('restart')
const onSubmit = () => emit('submit')
const onHistory = () => {
  // 跳转到历史记录页面
  router.push('/quiz/history')
}

const formattedReport = computed(() => {
  return JSON.stringify(props.report, null, 2)
})

// 计算答题数量
const totalQuestions = computed(() => {
  if (!props.report || !props.report.answers) return 0
  return Object.keys(props.report.answers).length
})

// 计算测验用时显示
const durationDisplay = computed(() => {
  if (!props.report || !props.report.durationMs) return '0秒'
  const duration = Math.floor(props.report.durationMs / 1000)
  if (duration < 60) {
    return `${duration}秒`
  } else if (duration < 3600) {
    const minutes = Math.floor(duration / 60)
    const seconds = duration % 60
    return `${minutes}分${seconds}秒`
  } else {
    const hours = Math.floor(duration / 3600)
    const minutes = Math.floor((duration % 3600) / 60)
    return `${hours}小时${minutes}分`
  }
})

// 计算平均每题用时
const avgTimePerQuestion = computed(() => {
  if (!props.report || !props.report.durationMs || totalQuestions.value === 0) return '0秒'
  const avgSeconds = Math.floor(props.report.durationMs / 1000 / totalQuestions.value)
  if (avgSeconds < 60) {
    return `${avgSeconds}秒`
  } else {
    const minutes = Math.floor(avgSeconds / 60)
    const seconds = avgSeconds % 60
    return `${minutes}分${seconds}秒`
  }
})
</script>

<style scoped>
button {
  transition: all 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

button:active {
  transform: translateY(0);
}
</style>