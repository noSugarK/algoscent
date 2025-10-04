<template>
  <AppHeader />
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">
          我的测验历史
        </h1>
        <p class="text-gray-600">
          查看你过去完成的所有香氛偏好测试记录
        </p>
      </div>

      <!-- Back to Home Button -->
      <div class="mb-8 flex justify-start">
        <router-link
          to="/quiz"
          class="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回测试主页
        </router-link>
      </div>

      <!-- History List -->
      <div v-if="loading" class="bg-white rounded-xl shadow-md p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
        <p class="text-gray-600">正在加载历史记录...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-8">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="historySessions.length === 0" class="bg-white rounded-xl shadow-md p-8 text-center">
        <svg class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">暂无测验记录</h3>
        <p class="text-gray-600 mb-6">你还没有完成任何测验，快来体验一下吧！</p>
        <router-link
          to="/quiz/question"
          class="px-6 py-2 bg-indigo-500 text-white font-medium rounded-lg hover:bg-indigo-600 transition-colors"
        >
          开始第一次测试
        </router-link>
      </div>

      <div v-else class="space-y-6">
        <!-- 成功提示 -->
        <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-400 p-4 rounded-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-green-700">{{ successMessage }}</p>
            </div>
          </div>
        </div>

        <!-- 未完成的测验记录 -->
        <div v-if="incompleteSessions.length > 0" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="px-6 py-4 bg-gray-50 border-b border-gray-100">
            <h2 class="text-lg font-semibold text-gray-800">未完成的测验 ({{ incompleteSessions.length }})</h2>
          </div>
          <div class="divide-y divide-gray-100">
            <div
              v-for="session in incompleteSessions"
              :key="session.id"
              class="px-6 py-4 hover:bg-gray-50 transition-colors cursor-pointer"
              @click="viewReport(session.session_id)"
            >
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <div class="flex items-center">
                  <div>
                    <div class="flex items-center">
                      <h3 class="text-lg font-medium text-gray-800">香氛偏好测验</h3>
                      <span 
                        class="bg-yellow-100 text-yellow-800 ml-3 px-2.5 py-0.5 rounded-full text-xs font-medium"
                      >
                        未完成
                      </span>
                    </div>
                    <p class="text-sm text-gray-500 mt-1">
                      开始时间: {{ formatDate(session.start_time) }}
                    </p>
                  </div>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-4 flex items-center space-x-3">
                  <div class="flex items-center text-sm text-gray-600">
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                      {{ session.answers_count || 0 }}/{{ session.total_questions || 0 }}题
                    </span>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click.stop="handleContinueSession(session)"
                      class="px-3 py-1.5 bg-indigo-500 hover:bg-indigo-600 text-white text-xs font-medium rounded transition-colors"
                    >
                      继续
                    </button>
                    <button 
                      @click.stop="handleDeleteSession(session)"
                      class="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white text-xs font-medium rounded transition-colors"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 已完成的测验记录 -->
        <div v-if="completedSessions.length > 0" class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="px-6 py-4 bg-gray-50 border-b border-gray-100">
            <h2 class="text-lg font-semibold text-gray-800">已完成的测验 ({{ completedSessions.length }})</h2>
          </div>
          <div class="divide-y divide-gray-100">
            <div
              v-for="session in completedSessions"
              :key="session.id"
              class="px-6 py-4 hover:bg-gray-50 transition-colors cursor-pointer"
              @click="viewReport(session.session_id)"
            >
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <div class="flex items-center">
                  <div>
                    <div class="flex items-center">
                      <h3 class="text-lg font-medium text-gray-800">香氛偏好测验</h3>
                      <span 
                        class="bg-green-100 text-green-800 ml-3 px-2.5 py-0.5 rounded-full text-xs font-medium"
                      >
                        已完成
                      </span>
                    </div>
                    <p class="text-sm text-gray-500 mt-1">
                      完成时间: {{ formatDate(session.completed_at) }}
                    </p>
                  </div>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-4 flex items-center space-x-3">
                  <div class="flex items-center text-sm text-gray-600">
                    <svg class="h-4 w-4 mr-1 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    用时: {{ formatDuration(session.time_spent) }}
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click.stop="viewReport(session)"
                      class="px-3 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-800 text-xs font-medium rounded transition-colors"
                    >
                      报告
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 记录数量限制提示 -->
        <div v-if="historySessions.length >= 10" class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-blue-700">已显示最近的10条测验记录</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getQuizHistory, resumeIncompleteSession, deleteIncompleteSession } from '@/api/quiz.api.js'
import AppHeader from "@/components/layout/AppHeader.vue";
import AppFooter from "@/components/layout/AppFooter.vue";

const router = useRouter()
const historySessions = ref([])
const loading = ref(false)
const error = ref('')
const successMessage = ref('')

// 状态文本映射
const statusTextMap = {
  'completed': '已完成',
  'in_progress': '未完成',
  'abandoned': '已放弃'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// 格式化时长
const formatDuration = (milliseconds) => {
  if (!milliseconds || milliseconds === null || milliseconds === undefined) return '未知'
  const seconds = Math.floor(milliseconds / 1000)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

// 加载历史记录
const loadHistory = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getQuizHistory()
    
    // 添加调试信息，查看返回的数据结构
    console.log('Quiz history response:', response)
    console.log('Quiz history data:', response.data)
    
    // 确保数据结构正确
    let formattedSessions = response.data.map(session => ({
      id: session.session_id || session.id,
      session_id: session.session_id,
      status: session.status || 'completed', // 保留状态信息
      start_time: session.start_time,
      completed_at: session.completed_at || session.end_time,
      time_spent: session.time_spent || session.duration_ms || 0,
      total_questions: session.total_questions || (session.answers ? session.answers.length : 0),
      answers_count: session.answers_count || (session.answers ? Object.keys(session.answers).length : 0)
    }))
    
    // 按开始时间降序排序（最新的在前）
    formattedSessions = formattedSessions.sort((a, b) => 
      new Date(b.start_time) - new Date(a.start_time)
    )
    
    // 限制最多显示10条记录
    historySessions.value = formattedSessions.slice(0, 10)
  } catch (err) {
    console.error('Failed to load quiz history:', err)
    error.value = '加载历史记录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 删除未完成的会话
const handleDeleteSession = async (session) => {
  if (session.status !== 'in_progress') return
  
  // 确认删除
  if (!confirm('确定要删除这条未完成的测验记录吗？')) {
    return
  }
  
  try {
    await deleteIncompleteSession(session.session_id)
    // 删除成功后重新加载历史记录
    successMessage.value = '删除成功'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
    await loadHistory()
  } catch (err) {
    console.error('删除会话失败:', err)
    error.value = '删除记录失败，请稍后重试'
  }
}

// 已完成的会话
const completedSessions = computed(() => {
  return historySessions.value.filter(session => session.status === 'completed')
})

// 未完成的会话
const incompleteSessions = computed(() => {
  return historySessions.value.filter(session => session.status === 'in_progress')
})

// 查看报告
const viewReport = (session) => {
  // 只有已完成的会话才能查看报告
  if (session.status === 'completed') {
    router.push(`/quiz/report/${session.session_id}`)
  }
}

// 继续未完成的会话
const handleContinueSession = async (session) => {
  if (session.status !== 'in_progress') return
  
  try {
    // 获取未完成会话的详情和答案
    const result = await resumeIncompleteSession(session.session_id)
    // 使用路由参数传递会话ID，这样更可靠
    router.push({
      path: '/quiz/question',
      query: { sessionId: session.session_id }
    })
  } catch (err) {
    console.error('继续会话失败:', err)
    error.value = '继续测验失败，请稍后重试'
  }
}

// 组件挂载时加载历史记录
onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
/* 添加一些额外的样式来增强用户体验 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.divide-y > div {
  animation: fadeIn 0.3s ease-out forwards;
}

.divide-y > div:nth-child(1) { animation-delay: 0.1s; }
.divide-y > div:nth-child(2) { animation-delay: 0.2s; }
.divide-y > div:nth-child(3) { animation-delay: 0.3s; }
.divide-y > div:nth-child(4) { animation-delay: 0.4s; }
.divide-y > div:nth-child(5) { animation-delay: 0.5s; }
</style>