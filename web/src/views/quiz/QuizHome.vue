<template>
  <AppHeader />
  <div class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4 flex items-center justify-center">
    <!-- 首页 -->
    <div v-if="!showQuiz" class="max-w-3xl mx-auto bg-white rounded-3xl shadow-xl p-10 md:p-12 border border-gray-100">
      <div class="text-center mb-10">
        <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-6">
          🌿 疗愈香氛偏好测试
        </h1>
        <p class="text-gray-600 text-lg leading-relaxed">
          帮助我们了解你的情绪、审美与生活方式，为你定制专属疗愈香氛方案。
        </p>
      </div>

      <div class="bg-gray-50 rounded-2xl p-8 mb-8 text-left space-y-4">
        <h3 class="font-bold text-gray-800 text-lg">📋 问卷说明</h3>
        <ul class="list-disc list-inside space-y-2 text-gray-700">
          <li>共4个部分，约20题，预计耗时10分钟</li>
          <li>所有信息仅用于香氛推荐，严格保密</li>
          <li>请根据第一直觉作答，无对错之分</li>
          <!-- li>部分题目会根据你的选择动态调整</li -->
        </ul>
      </div>

      <div class="flex items-center mb-8">
        <input
            id="agree"
            type="checkbox"
            v-model="agreed"
            class="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
        />
        <label for="agree" class="ml-3 text-gray-700">
          我已阅读并同意以上说明，自愿参与测试
        </label>
      </div>

      <div class="flex flex-col sm:flex-row gap-4">
        <button
            @click="handleStartQuiz"
            :disabled="!agreed || loading"
            class="flex-1 py-4 px-8 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 text-white font-bold rounded-xl text-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed"
        >
          <span v-if="loading">⏳ 检查中...</span>
          <span v-else>🚀 开始测试</span>
        </button>
        <router-link
            to="/quiz/history"
            class="flex-1 py-4 px-8 bg-white border border-gray-300 hover:border-indigo-300 text-gray-800 font-bold rounded-xl text-lg transition-all hover:bg-gray-50 flex items-center justify-center"
        >
          📋 查看历史记录
        </router-link>
      </div>

      <div class="mt-8 text-center text-sm text-gray-500">
        点击开始即表示你授权我们基于你的答案生成个性化推荐
      </div>
    </div>

    <!-- 问卷内容通过路由跳转显示 -->
  </div>
  <AppFooter />

  <!-- 未完成会话确认弹窗 -->
  <div v-if="showIncompleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
      <div class="text-center mb-6">
        <h3 class="text-2xl font-bold text-gray-800 mb-2">发现未完成的测试</h3>
        <p class="text-gray-600">我们检测到你之前有一次未完成的测试会话</p>
      </div>
      <div class="bg-gray-50 rounded-xl p-6 mb-6">
        <div class="flex justify-between items-center mb-3">
          <span class="text-gray-600">开始时间</span>
          <span class="font-medium text-gray-800">{{ formatDate(incompleteSession?.start_time) }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-gray-600">已完成进度</span>
          <span class="font-medium text-gray-800">{{ incompleteSession?.answers_count || 0 }}/{{ incompleteSession?.total_questions || 0 }}题</span>
        </div>
      </div>
      <div class="flex flex-col sm:flex-row gap-4">
        <button
            @click="continuePreviousSession"
            class="flex-1 py-3 px-6 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold rounded-xl transition-all transform hover:scale-105"
        >
          继续测试
        </button>
        <button
            @click="startNewSession"
            class="flex-1 py-3 px-6 bg-white border border-gray-300 text-gray-800 font-bold rounded-xl transition-all hover:bg-gray-50"
        >
          重新开始
        </button>
      </div>
    </div>
  </div>
  
  <!-- 测验数量超限提示 -->
  <div v-if="showMaxSessionsError" class="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in">
    <div class="flex items-center">
      <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>您的测验记录已达10条上限，无法开始新测验</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from "@/components/layout/AppHeader.vue";
import AppFooter from "@/components/layout/AppFooter.vue";
import { checkIncompleteSession, getQuizHistory } from '@/api/quiz.api.js';

// 初始化router
const router = useRouter()

const agreed = ref(false)
const loading = ref(false)
const showIncompleteDialog = ref(false)
const incompleteSession = ref(null)
const showMaxSessionsError = ref(false)
// 保留showQuiz变量以避免模板中的引用错误
const showQuiz = ref(false)

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

// 处理开始测验
const handleStartQuiz = async () => {
  if (!agreed.value) return
  
  loading.value = true
  try {
    // 检查用户测验历史记录数量
    const historyResponse = await getQuizHistory()
    const totalSessions = historyResponse.data.length
    
    // 如果测验总数大于等于10条，不允许开始新测验
    if (totalSessions >= 10) {
      showMaxSessionsError.value = true
      setTimeout(() => {
        showMaxSessionsError.value = false
      }, 3000)
      return
    }
    
    // 检查是否有未完成的会话
    const response = await checkIncompleteSession()
    if (response.data.has_incomplete) {
      // 有未完成的会话，显示确认对话框
      incompleteSession.value = response.data
      showIncompleteDialog.value = true
    } else {
      // 没有未完成的会话，直接开始新测试
      startNewSession()
    }
  } catch (error) {
    console.error('检查未完成会话失败:', error)
    // 出错时默认开始新测试
    startNewSession()
  } finally {
    loading.value = false
  }
}

// 继续之前的会话
const continuePreviousSession = async () => {
  if (!incompleteSession.value?.session_id) return
  
  loading.value = true
  showIncompleteDialog.value = false
  try {
    console.log('🔄 从首页继续会话，sessionId:', incompleteSession.value.session_id)
    // 使用路由参数传递会话ID，与History.vue保持一致的方式
    router.push({
      path: '/quiz/question',
      query: { sessionId: incompleteSession.value.session_id }
    })
  } catch (error) {
    console.error('继续会话失败:', error)
    // 出错时默认开始新测试
    startNewSession()
  } finally {
    loading.value = false
  }
}

// 开始新会话
const startNewSession = () => {
  showIncompleteDialog.value = false
  console.log('🚀 开始新测试，跳转到题目页面')
  // 直接跳转到题目页面，不传递sessionId会自动创建新会话
  router.push('/quiz/question')
}

// 由于使用路由跳转，QuizHome不再处理问卷完成和重启逻辑
// 这些逻辑在Question组件和路由层面处理

</script>

<style>
/* 动画效果 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>