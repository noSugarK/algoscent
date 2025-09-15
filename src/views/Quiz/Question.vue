<!-- src/components/quiz/QuizComponent.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          疗愈香氛偏好测试
        </h1>
        <p class="text-gray-600">第 {{ visibleQuestionIndex + 1 }} 题 / 共 {{ totalVisibleQuestions }} 题</p>
      </div>

      <!-- Result View -->
      <ResultDisplay
        v-if="completed"
        :report="getReport()"
        @restart="handleRestart"
        @submit="handleSubmit"
        class="animate-fadeIn"
      />

      <!-- Quiz View -->
      <div v-else-if="currentQuestion" class="bg-white rounded-3xl shadow-xl p-8 md:p-10 border border-gray-100 animate-slideUp">
        <!-- Group Title -->
        <div v-if="showGroupTitle" class="mb-8 text-center bg-gray-50 rounded-2xl p-6 -mx-8 md:-mx-10">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ currentGroup.title }}</h2>
          <p class="text-gray-600">{{ currentGroup.description }}</p>
        </div>

        <!-- Question -->
        <div class="mb-8">
          <h3 class="text-xl font-medium text-gray-800 mb-6">{{ currentQuestion.text }}</h3>
        </div>

        <!-- Dynamic Question Component -->
        <component
          :is="getComponentForQuestion(currentQuestion)"
          :question="currentQuestion"
          v-model:answer="tempAnswer"
          v-model:multiAnswer="tempMultiAnswer"
          v-model:textAnswer="tempTextAnswer"
          @update="onAnswerUpdate"
        />

        <!-- Navigation -->
        <div class="flex flex-col sm:flex-row justify-between gap-4 mt-10 pt-6 border-t border-gray-100">
          <button
            v-if="visibleQuestionIndex > 0"
            @click="prevQuestion"
            class="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-xl transition-colors transform hover:-translate-y-1"
          >
            ← 上一题
          </button>
          <div></div>
          <button
            @click="nextQuestion"
            :disabled="!isAnswered"
            :class="[
              'px-6 py-3 font-medium rounded-xl transition-all transform',
              isAnswered
                ? 'bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white hover:scale-105'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            ]"
          >
            {{ visibleQuestionIndex === visibleQuestions.length - 1 ? '完成测试' : '下一题 →' }}
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-else class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, markRaw } from 'vue'
import { questionGroups } from '@/data/questions.js'
import ResultDisplay from '@/components/quiz/ResultDisplay.vue'

// 题型组件
import Part1 from '@/components/quiz/Part1.vue'
import Part2 from '@/components/quiz/Part2.vue'
import Part3 from '@/components/quiz/Part3.vue'
import Part4 from '@/components/quiz/Part4.vue'

// ===== 定义事件 =====
const emit = defineEmits(['complete', 'restart'])

// ===== 状态 =====
const answers = ref({})
const completed = ref(false)
const startTime = ref(Date.now())

// 临时答案
const tempAnswer = ref('')
const tempMultiAnswer = ref([])
const tempTextAnswer = ref('')

// 构建题目序列
const allQuestionsWithGroup = ref([])
const visibleQuestions = ref([])
const currentVisibleIndex = ref(0)

onMounted(() => {
  initQuestions()
  updateVisibleQuestions()
})

const initQuestions = () => {
  allQuestionsWithGroup.value = []
  questionGroups.forEach(group => {
    group.questions.forEach(q => {
      allQuestionsWithGroup.value.push({
        groupId: group.id,
        groupTitle: group.title,
        groupDescription: group.description,
        ...q
      })
    })
  })
}

const updateVisibleQuestions = () => {
  const result = []
  for (const q of allQuestionsWithGroup.value) {
    if (!q.condition || q.condition(answers.value)) {
      result.push(q)
    }
  }
  visibleQuestions.value = result
  if (currentVisibleIndex.value >= visibleQuestions.value.length && visibleQuestions.value.length > 0) {
    currentVisibleIndex.value = visibleQuestions.value.length - 1
  }
  loadCurrentQuestionState()
}

watch(answers, () => updateVisibleQuestions(), { deep: true })

// ===== 计算属性 =====
const currentQuestion = computed(() => visibleQuestions.value[currentVisibleIndex.value])
const currentGroup = computed(() => currentQuestion.value ? {
  title: currentQuestion.value.groupTitle,
  description: currentQuestion.value.groupDescription
} : {})

const showGroupTitle = computed(() => {
  if (!currentQuestion.value) return false
  const currentIndex = currentVisibleIndex.value
  for (let i = currentIndex - 1; i >= 0; i--) {
    if (visibleQuestions.value[i].groupId === currentQuestion.value.groupId) {
      return false
    }
  }
  return true
})

const visibleQuestionIndex = computed(() => currentVisibleIndex.value)
const totalVisibleQuestions = computed(() => visibleQuestions.value.length)

const isAnswered = computed(() => {
  const q = currentQuestion.value
  if (!q) return false

  if (q.type === 'single' || q.type === 'image-single') {
    return !!tempAnswer.value
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    return tempMultiAnswer.value.length >= (q.minSelection || 1) &&
           tempMultiAnswer.value.length <= (q.maxSelection || Infinity)
  } else if (q.type === 'single-with-text') {
    if (!tempAnswer.value) return false
    if (tempAnswer.value === q.showTextWhen) {
      return !!tempTextAnswer.value.trim()
    }
    return true
  } else if (q.type === 'text') {
    return !!tempTextAnswer.value.trim()
  }
  return false
})

const componentMap = {
  'single': markRaw(Part1),
  'single-with-text': markRaw(Part2),
  'image-single': markRaw(Part3),
  'image-multiple': markRaw(Part4)
}

const getComponentForQuestion = (q) => componentMap[q.type] || 'div'

// ===== 方法 =====
const loadCurrentQuestionState = () => {
  const q = currentQuestion.value
  if (!q) return

  const saved = answers.value[q.id]
  if (q.type === 'single' || q.type === 'image-single') {
    tempAnswer.value = saved?.value || ''
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    tempMultiAnswer.value = Array.isArray(saved) ? [...saved] : []
  } else if (q.type === 'single-with-text' || q.type === 'text') {
    if (saved) {
      tempAnswer.value = saved.value || ''
      tempTextAnswer.value = saved.text || ''
    } else {
      tempAnswer.value = ''
      tempTextAnswer.value = ''
    }
  }
}

const saveAnswer = () => {
  const q = currentQuestion.value
  if (!q) return

  if (q.type === 'single' || q.type === 'image-single') {
    answers.value[q.id] = { value: tempAnswer.value }
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    answers.value[q.id] = [...tempMultiAnswer.value]
  } else if (q.type === 'single-with-text') {
    answers.value[q.id] = {
      value: tempAnswer.value,
      text: tempAnswer.value === q.showTextWhen ? tempTextAnswer.value : ''
    }
  } else if (q.type === 'text') {
    answers.value[q.id] = tempTextAnswer.value
  }
}

const onAnswerUpdate = () => {}

const nextQuestion = () => {
  if (!isAnswered.value) return
  saveAnswer()

  if (currentVisibleIndex.value === totalVisibleQuestions.value - 1) {
    completed.value = true
    emit('complete', getReport()) // ✅ 发出完成事件
  } else {
    currentVisibleIndex.value++
    setTimeout(() => loadCurrentQuestionState(), 50)
  }
}

const prevQuestion = () => {
  saveAnswer()
  currentVisibleIndex.value--
  loadCurrentQuestionState()
}

const handleSubmit = () => {
  const report = getReport()
  console.log('📝 提交报告:', report)
  alert('感谢参与！你的专属香氛报告已生成。')
}

const handleRestart = () => {
  emit('restart') // ✅ 发出重启事件
}

// ✅ 暴露 reset 方法供父组件调用
const reset = () => {
  answers.value = {}
  completed.value = false
  startTime.value = Date.now()
  currentVisibleIndex.value = 0
  tempAnswer.value = ''
  tempMultiAnswer.value = []
  tempTextAnswer.value = ''
  initQuestions()
  updateVisibleQuestions()
}

defineExpose({
  reset
})

const getReport = () => ({
  id: 'AROMA_' + Date.now(),
  startTime: new Date(startTime.value).toISOString(),
  endTime: new Date().toISOString(),
  durationMs: Date.now() - startTime.value,
  answers: { ...answers.value },
  completedAt: new Date().toLocaleString()
})
</script>

<style scoped>
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.animate-fadeIn { animation: fadeIn 0.6s ease-out forwards; }
.animate-slideUp { animation: slideUp 0.5s ease-out forwards; }
</style>