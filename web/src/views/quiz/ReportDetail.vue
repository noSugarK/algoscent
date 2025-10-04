<template>
  <AppHeader />
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">
          疗愈香氛推荐报告
        </h1>
      </div>

      <!-- Navigation -->
      <div class="mb-8 flex justify-between flex-wrap gap-4">
        <router-link
          to="/quiz/history"
          class="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回历史记录
        </router-link>
        <button
          @click="takeNewQuiz"
          class="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          重新测试
        </button>
      </div>

      <!-- Loading/Error State -->
      <div v-if="loading" class="bg-white rounded-xl shadow-md p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
        <p class="text-gray-600">正在加载报告...</p>
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

      <!-- Report Content -->
      <div v-else class="space-y-8">
        <!-- Quiz Info -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">测验信息</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500 mb-1">完成时间</p>
              <p class="font-medium text-gray-800">{{ formatDate(reportData.completed_at) }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500 mb-1">用时</p>
              <p class="font-medium text-gray-800">{{ formatDuration(reportData.time_spent) }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500 mb-1">题目数量</p>
              <p class="font-medium text-gray-800">{{ reportData.total_questions }}题</p>
            </div>
          </div>
        </div>

        <!-- Personality Insights -->
        <div class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg p-8 text-white">
          <h2 class="text-xl font-semibold mb-4">你的性格香氛洞察</h2>
          <div class="space-y-4">
            <div v-for="insight in personalityInsights" :key="insight.title" class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <h3 class="font-medium text-lg mb-2">{{ insight.title }}</h3>
              <p>{{ insight.description }}</p>
            </div>
          </div>
        </div>

        <!-- Recommended Scents -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">推荐香氛类型</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div
              v-for="scent in recommendedScents"
              :key="scent.id"
              class="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition-colors"
            >
              <div class="flex items-start">
                <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                  <span class="text-xl">{{ scent.emoji }}</span>
                </div>
                <div>
                  <h3 class="font-medium text-gray-800 mb-1">{{ scent.name }}</h3>
                  <p class="text-sm text-gray-600">{{ scent.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Answer Details -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">答题详情</h2>
            <button
              @click="toggleAnswerDetails"
              class="text-indigo-600 hover:text-indigo-800 transition-colors flex items-center"
            >
              {{ showAnswerDetails ? '隐藏详情' : '查看详情' }}
              <svg
                :class="{ 'rotate-180': showAnswerDetails }"
                xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transition-transform duration-300"
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <transition name="slide-fade">
            <div v-if="showAnswerDetails" class="divide-y divide-gray-100">
              <div
                v-for="answer in userAnswers"
                :key="answer.question_id"
                class="py-4"
              >
                <div class="mb-2">
                  <span class="text-sm font-medium text-gray-900">
                    问题 {{ answer.question_index }}: {{ answer.question_text }}
                  </span>
                </div>
                <div class="ml-4">
                  <span class="text-sm text-gray-600">你的回答: </span>
                  <span class="text-sm font-medium text-indigo-600">
                    <!-- 优先显示选项文本，如果没有则显示原始值 -->
                    {{ answer.option_label || (answer.value !== null && answer.value !== undefined ? JSON.stringify(answer.value) : '无回答') }}
                  </span>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Share and Action Buttons -->
        <div class="bg-white rounded-xl shadow-md p-6 text-center">
          <p class="text-gray-700 mb-4">想要体验更多？保存这份报告或尝试新的测试！</p>
          <div class="flex flex-wrap justify-center gap-4">
            <button
              @click="exportReport"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              导出报告
            </button>
            <button
              @click="shareReport"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
              </svg>
              分享报告
            </button>
            <button
              @click="takeNewQuiz"
              class="px-6 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              重新测试
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getQuizReport } from '@/api/quiz.api.js'
import AppFooter from "@/components/layout/AppFooter.vue";
import AppHeader from "@/components/layout/AppHeader.vue";

const router = useRouter()
const route = useRoute()
const sessionId = route.params.sessionId

const reportData = ref({})
const userAnswers = ref([])
const loading = ref(false)
const error = ref('')
const showAnswerDetails = ref(false)

// 根据用户数据生成的性格洞察
const personalityInsights = ref([
  {
    title: "你的性格特质",
    description: "基于你的回答，我们发现你是一个喜欢探索和创新的人，倾向于选择独特且富有个性的香氛。"
  },
  {
    title: "情绪与香氛关联",
    description: "你在压力情境下倾向于寻求平静和放松，木质和香草调的香氛可能会特别适合你。"
  },
  {
    title: "生活方式匹配",
    description: "你的生活方式偏向于平衡和多样化，适合尝试不同香调的组合，以适应不同的场合和心情。"
  }
])

// 推荐的香氛类型
const recommendedScents = ref([
  {
    id: 1,
    name: "木质调香氛",
    description: "温暖、沉稳的木质香气，帮助你在忙碌的生活中找到宁静。",
    emoji: "🌲"
  },
  {
    id: 2,
    name: "花香调香氛",
    description: "清新、优雅的花香，为你的日常增添一抹浪漫和愉悦。",
    emoji: "🌸"
  },
  {
    id: 3,
    name: "柑橘调香氛",
    description: "活力、明快的柑橘香气，提升你的精神状态和创造力。",
    emoji: "🍊"
  },
  {
    id: 4,
    name: "香草调香氛",
    description: "甜美、舒适的香草气息，为你营造温馨的氛围。",
    emoji: "🌿"
  }
])

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

// 格式化时长（参数是毫秒）
const formatDuration = (milliseconds) => {
  if (!milliseconds || milliseconds === null || milliseconds === undefined) return '未知'
  // 将毫秒转换为秒
  const seconds = Math.floor(milliseconds / 1000)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

// 加载报告数据
const loadReport = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getQuizReport(sessionId)
    reportData.value = response.data
    
    // 从响应中提取用户答案并转换为数组
    if (response.data.answers) {
      // 将答案对象转换为数组并添加索引
      userAnswers.value = Object.values(response.data.answers).map((answer, index) => ({
        ...answer,
        question_index: index + 1
      })).sort((a, b) => {
        return parseInt(a.question_index) - parseInt(b.question_index)
      })
    } else {
      userAnswers.value = []
    }
    
    // 根据实际数据更新洞察和推荐
    updateInsightsAndRecommendations()
  } catch (err) {
    console.error('Failed to load quiz report:', err)
    error.value = '加载报告失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 根据实际数据更新洞察和推荐
const updateInsightsAndRecommendations = () => {
  // 这里可以根据实际的答题数据进行更复杂的分析和推荐
  // 目前使用模拟数据，但结构保持一致
  console.log('Updating insights and recommendations based on user answers')
}

// 切换答题详情显示
const toggleAnswerDetails = () => {
  showAnswerDetails.value = !showAnswerDetails.value
}

// 导出报告
const exportReport = () => {
  alert('报告导出功能将在未来版本中提供')
  // 实际实现中可以生成PDF或其他格式的报告
}

// 分享报告
const shareReport = () => {
  alert('报告分享功能将在未来版本中提供')
  // 实际实现中可以使用Web Share API或生成分享链接
}

// 重新测试
const takeNewQuiz = () => {
  router.push('/quiz/question')
}

// 组件挂载时加载报告数据
onMounted(() => {
  loadReport()
})
</script>

<style scoped>
/* 添加一些动画效果 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* 为推荐香氛卡片添加悬停效果 */
.grid > div:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
</style>