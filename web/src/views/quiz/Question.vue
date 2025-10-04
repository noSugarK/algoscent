<template>
  <AppHeader />
  <div class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4">
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
      <div v-else-if="currentQuestion"
           class="bg-white rounded-3xl shadow-xl p-8 md:p-10 border border-gray-100 animate-slideUp">
        <!-- Group Title -->
        <div class="mb-8 text-center bg-gray-50 rounded-2xl p-6 -mx-8 md:-mx-10">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ currentGroup.title }}</h2>
          <p class="text-gray-600">{{ currentGroup.description }}</p>
        </div>

        <!-- Question -->
        <div class="flex items-center justify-between mb-8">
          <h3 class="text-xl font-medium text-gray-800 flex-grow">{{ currentQuestion.text }}</h3>
          <button
              v-if="currentQuestion.type === 'image-single'"
              @click="shuffleImages(currentQuestion)"
              class="flex items-center space-x-2 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-xl transition-colors">
            <span>换一组</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
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
              :disabled="!isAnswered || loading"
              :class="[
              'px-6 py-3 font-medium rounded-xl transition-all transform',
              isAnswered && !loading
                ? 'bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white hover:scale-105'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            ]"
          >
            {{ loading ? '处理中...' : (visibleQuestionIndex === visibleQuestions.length - 1 ? '完成测试' : '下一题 →') }}
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-else-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        <p class="mt-4 text-gray-600">加载题目中...</p>
      </div>
      
      <!-- Error -->
      <div v-else-if="error" class="text-center py-20">
        <div class="inline-block p-4 bg-red-100 rounded-full mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">加载失败</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button 
          @click="initQuestions()" 
          class="px-6 py-3 bg-indigo-500 hover:bg-indigo-600 text-white font-medium rounded-xl transition-colors"
        >
          重试
        </button>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import {ref, computed, onMounted, watch, markRaw} from 'vue'
import {useRoute} from 'vue-router'
import {getQuestionGroups, createQuizSession, saveUserAnswer, completeQuizSession, resumeIncompleteSession} from '@/api/quiz.api.js'
import ResultDisplay from '@/components/quiz/ResultDisplay.vue'

// 题型组件
import Single from '@/components/quiz/Single.vue'
import Multiple from "@/components/quiz/Multiple.vue";
import SingleWithText from '@/components/quiz/SingleWithText.vue'
import ImageSingle from '@/components/quiz/ImageSingle.vue'
import ImageMultiple from '@/components/quiz/ImageMultiple.vue'
import Text from '@/components/quiz/Text.vue'
import AppHeader from "@/components/layout/AppHeader.vue";
import AppFooter from "@/components/layout/AppFooter.vue";

// 打乱数组顺序的工具函数
const shuffleArray = (array) => {
  const newArray = [...array];
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
  }
  return newArray;
}

// 接收初始会话数据
const props = defineProps({
  initialSession: {
    type: Object,
    default: null
  }
})

// ===== 定义事件 =====
const emit = defineEmits(['complete', 'restart'])

// ===== 状态 =====
const answers = ref({})
const completed = ref(false)
const startTime = ref(Date.now())
const sessionId = ref('')
const loading = ref(false)
const error = ref('')
const loadedSessionData = ref(null)

// 路由
const route = useRoute()

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
})

const initQuestions = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // 检查路由参数中是否有sessionId
    const sessionIdFromRoute = route.query.sessionId
    // console.log('🔍 检查路由参数sessionId:', sessionIdFromRoute)
    
    // 如果有sessionId参数，尝试恢复会话
    if (sessionIdFromRoute) {
      try {
        // console.log('🔄 尝试恢复会话:', sessionIdFromRoute)
        const result = await resumeIncompleteSession(sessionIdFromRoute)
        // console.log('✅ 恢复会话数据:', result)
        loadedSessionData.value = result
      } catch (sessionError) {
        // console.error('恢复会话失败:', sessionError)
        error.value = '恢复会话失败，开始新会话'
        // 继续执行，会自动创建新会话
      }
    } else {
      console.log('🚫 没有从路由参数获取到sessionId')
    }
    
    // 获取题目组数据
    const groupsData = await getQuestionGroups()
    
    // 构建题目序列
    allQuestionsWithGroup.value = []
    
    // 处理可能的分页响应格式
    const groupsArray = Array.isArray(groupsData) ? groupsData : (groupsData.results || [])
    
    if (groupsArray.length === 0) {
      console.warn('没有获取到题目数据')
      // 可以添加一些默认的模拟数据，防止页面空白
      allQuestionsWithGroup.value = [
        {
          id: 'demo-1',
          groupId: 'demo-group',
          groupTitle: '示例题目组',
          groupDescription: '这是一个示例题目组',
          text: '你喜欢哪种类型的香氛？',
          type: 'single',
          options: [
            { label: 'A', value: 'floral', text: '花香调' },
            { label: 'B', value: 'woody', text: '木质调' },
            { label: 'C', value: 'citrus', text: '柑橘调' },
            { label: 'D', value: 'spicy', text: '辛辣调' }
          ]
        }
      ]
    } else {
      groupsArray.forEach(group => {
        // 确保questions存在且为数组
        if (group.questions && Array.isArray(group.questions)) {
          group.questions.forEach(q => {
            // 优先使用数据库中的max_selection字段，兼容maxSelection
            // console.log(q)
            const calculatedMaxSelection = q.max_selection || q.maxSelection;
            // console.log(`🔧 初始化题目ID: ${q.id}, 类型: ${q.type}, max_selection: ${q.max_selection}, maxSelection: ${q.maxSelection}, calculatedMaxSelection: ${calculatedMaxSelection}`);
            
            allQuestionsWithGroup.value.push({
              id: q.id,
              groupId: group.id,
              groupTitle: group.title,
              groupDescription: group.description,
              imageRange: group.imageRange || 1,
              imagesPath: group.imagesPath || '',
              text: q.text,
              type: q.type,
              options: q.options || [],
              minSelection: q.minSelection || 1,
              maxSelection: calculatedMaxSelection,
              showTextWhen: q.showTextWhen,
              condition: q.condition
            })
          })
        }
      })
    }
    
    // 检查是否有初始会话数据（继续之前的会话）
    // console.log('🔍 检查初始会话数据 - props.initialSession:', props.initialSession)
    // console.log('🔍 检查初始会话数据 - loadedSessionData.value:', loadedSessionData.value)
    
    if ((props.initialSession && props.initialSession.session_id) || loadedSessionData.value) {
      // console.log('✅ 检测到会话数据，准备恢复')
      // 使用之前的会话ID
      const sessionData = props.initialSession || loadedSessionData.value
      
      // 确保answers.value初始化为空对象
      answers.value = {};
      
      // 检查数据格式，确保正确提取数据
      if (sessionData.session) {
        // console.log('📋 使用resumeIncompleteSession返回的格式')
        // 这是从resumeIncompleteSession返回的格式
        sessionId.value = sessionData.session.session_id
        startTime.value = sessionData.session.start_time ? new Date(sessionData.session.start_time).getTime() : Date.now()
        
        // 正确处理answerMap格式的答案数据
        if (sessionData.answers && typeof sessionData.answers === 'object') {
          // console.log('📥 加载答案数据:', sessionData.answers)
          answers.value = {...sessionData.answers}
        } else if (sessionData.session.answers && Array.isArray(sessionData.session.answers)) {
          // 处理直接包含在session对象中的答案数组
          // console.log('📥 加载嵌套在session中的答案数组:', sessionData.session.answers)
          sessionData.session.answers.forEach(answer => {
            if (answer.question_id) {
              answers.value[answer.question_id] = answer.value;
            }
          });
        }
        
        loadedSessionData.value = sessionData.session
      } else {
        // console.log('📋 使用props或其他方式传递的格式')
        // 这是从props或其他方式传递的格式
        sessionId.value = sessionData.session_id
        startTime.value = sessionData.start_time ? new Date(sessionData.start_time).getTime() : Date.now()
        
        if (sessionData.answers && typeof sessionData.answers === 'object') {
          console.log('📥 加载答案数据:', sessionData.answers)
          answers.value = {...sessionData.answers}
        }
        
        loadedSessionData.value = sessionData
      }
      
      // 验证答案数据是否正确加载
      if (Object.keys(answers.value).length > 0) {
        // console.log('✅ 恢复会话成功，已加载答案数:', Object.keys(answers.value).length)
        // console.log('✅ 当前会话ID:', sessionId.value)
        // console.log('✅ 加载的答案键:', Object.keys(answers.value))
      } else {
        console.log('⚠️ 未加载到任何答案数据')
      }
    } else {
      // 创建新的测验会话
      try {
        const sessionData = await createQuizSession()
        sessionId.value = sessionData.session_id
      } catch (sessionError) {
        console.warn('创建会话失败，使用临时会话ID:', sessionError)
        // 生成临时会话ID，确保功能可以继续使用
        sessionId.value = 'TEMP_' + Date.now()
      }
    }
    
    // 初始化可见题目
    updateVisibleQuestions()
    
    // 如果有会话数据，尝试找到最后回答的题目位置
    if (Object.keys(answers.value).length > 0) {
      // 找到最后回答的题目
      const answeredQuestions = Object.keys(answers.value)
      // console.log(answeredQuestions)
      // 找到该题目在visibleQuestions中的索引
      const lastAnsweredIndex = visibleQuestions.value.findIndex(q => answeredQuestions.includes(q.id))
      if (lastAnsweredIndex !== -1 && lastAnsweredIndex < visibleQuestions.value.length - 1) {
        // 如果找到且不是最后一题，设置为下一题
        currentVisibleIndex.value = answeredQuestions.length - 1
        console.log('✅ 定位到未完成题目位置:', currentVisibleIndex.value + 1)
        // 确保加载对应的题目状态
        setTimeout(() => loadCurrentQuestionState(), 100)
      }
    }
    
  } catch (err) {
    console.error('初始化题目失败:', err)
    error.value = `题目加载失败: ${err.message || '未知错误'}`
    
    // 添加错误时的模拟数据
    allQuestionsWithGroup.value = [
      {
        id: 'error-1',
        groupId: 'error-group',
        groupTitle: '示例题目组',
        groupDescription: '由于网络或服务器问题，无法加载题目。以下是示例题目。',
        text: '你喜欢哪种类型的香氛？',
        type: 'single',
        options: [
          { label: 'A', value: 'floral', text: '花香调' },
          { label: 'B', value: 'woody', text: '木质调' },
          { label: 'C', value: 'citrus', text: '柑橘调' },
          { label: 'D', value: 'spicy', text: '辛辣调' }
        ]
      }
    ]
    
    sessionId.value = 'TEMP_' + Date.now()
    updateVisibleQuestions()
  } finally {
    loading.value = false
  }
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

watch(answers, () => updateVisibleQuestions(), {deep: true})

// ===== 计算属性 =====
const currentQuestion = computed(() => visibleQuestions.value[currentVisibleIndex.value])
const currentGroup = computed(() => currentQuestion.value ? {
  title: currentQuestion.value.groupTitle,
  description: currentQuestion.value.groupDescription,
  imageRange: currentQuestion.value.imageRange,
  imagesPath: currentQuestion.value.imagesPath
} : {})

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
  'single': markRaw(Single),
  'multiple': markRaw(Multiple),
  'single-with-text': markRaw(SingleWithText),
  'image-single': markRaw(ImageSingle),
  'image-multiple': markRaw(ImageMultiple),
  'text': markRaw(Text)
}

const getComponentForQuestion = (q) => componentMap[q.type] || 'div'

// ===== 方法 =====
const loadCurrentQuestionState = () => {
  const q = currentQuestion.value
  if (!q) return

  // showTextWhen属性的处理现在在SingleWithText.vue组件内部进行，避免直接修改props

  // 打乱选择题选项顺序
  if (q.options && Array.isArray(q.options) && 
      (q.type === 'single' || q.type === 'multiple' || q.type === 'single-with-text')) {
    // 为了保持答案一致性，我们在打乱前创建一个副本
    q.shuffledOptions = shuffleArray([...q.options])
  }

  const saved = answers.value[q.id]
  if (q.type === 'single' || q.type === 'image-single') {
    tempAnswer.value = saved?.value || ''
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    // 处理字符串格式的数组或普通数组
    if (Array.isArray(saved)) {
      tempMultiAnswer.value = [...saved]
    } else if (typeof saved === 'string') {
      try {
        // 尝试解析字符串格式的数组
        const parsed = JSON.parse(saved)
        tempMultiAnswer.value = Array.isArray(parsed) ? [...parsed] : []
      } catch {
        tempMultiAnswer.value = []
      }
    } else {
      tempMultiAnswer.value = []
    }
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

const saveAnswer = async () => {
  const q = currentQuestion.value
  if (!q || !sessionId.value) return

  // 构建答案对象
  let answerData
  if (q.type === 'single' || q.type === 'image-single') {
    answerData = {value: tempAnswer.value}
    answers.value[q.id] = answerData
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    answerData = [...tempMultiAnswer.value]
    answers.value[q.id] = answerData
  } else if (q.type === 'single-with-text') {
      answerData = {
        value: tempAnswer.value,
        text: (tempAnswer.value === q.showTextWhen || tempAnswer.value === 'yes') ? tempTextAnswer.value : ''
      }
      answers.value[q.id] = answerData
  } else if (q.type === 'text') {
    answerData = tempTextAnswer.value
    answers.value[q.id] = answerData
  }
  
  // 保存到后端
  try {
    await saveUserAnswer(sessionId.value, q.id, answerData)
  } catch (err) {
    console.error('保存答案到后端失败:', err)
    // 这里可以选择是否提示用户保存失败
  }
}

const onAnswerUpdate = () => {
  console.log('📝 答案更新通知收到:', {
    currentQuestionId: currentQuestion.value?.id,
    tempMultiAnswer: [...tempMultiAnswer.value],
    isAnswered: isAnswered.value
  });
  // 显式保存答案，确保更新被正确处理
  // saveAnswer(); - 注释掉自动保存，避免频繁请求
}

const nextQuestion = async () => {
  if (!isAnswered.value || loading.value) return
  
  loading.value = true
  try {
    await saveAnswer()

    if (currentVisibleIndex.value === totalVisibleQuestions.value - 1) {
      // 完成测验
      await completeQuizSession(sessionId.value)
      completed.value = true
      emit('complete', getReport())
    } else {
      currentVisibleIndex.value++
      setTimeout(() => loadCurrentQuestionState(), 50)
    }
  } catch (err) {
    console.error('处理下一题失败:', err)
    error.value = `操作失败: ${err.message || '未知错误'}`
  } finally {
    loading.value = false
  }
}

const prevQuestion = async () => {
  if (loading.value) return
  
  loading.value = true
  try {
    await saveAnswer()
    currentVisibleIndex.value--
    loadCurrentQuestionState()
  } catch (err) {
    console.error('处理上一题失败:', err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  const report = getReport()
  console.log('📝 提交报告:', report)
  
  try {
    // 确保测验已经完成
    if (!completed.value && sessionId.value) {
      await completeQuizSession(sessionId.value)
    }
    alert('感谢参与！你的专属香氛报告已生成并保存。')
  } catch (err) {
    console.error('提交报告失败:', err)
    alert('保存报告失败，请稍后重试。')
  }
}

const handleRestart = () => {
  emit('restart')
}

// ✅ 暴露 reset 方法供父组件调用
const reset = () => {
  answers.value = {}
  completed.value = false
  startTime.value = Date.now()
  sessionId.value = ''
  currentVisibleIndex.value = 0
  tempAnswer.value = ''
  tempMultiAnswer.value = []
  tempTextAnswer.value = ''
  error.value = ''
  initQuestions()
}

defineExpose({
  reset
})

const getReport = () => ({
  id: sessionId.value || 'AROMA_' + Date.now(),
  startTime: new Date(startTime.value).toISOString(),
  endTime: new Date().toISOString(),
  durationMs: Date.now() - startTime.value,
  answers: {...answers.value},
  completedAt: new Date().toLocaleString(),
  // 如果是继续的会话，包含原始开始时间
  originalStartTime: loadedSessionData.value?.start_time || null
})

// 方法定义
const shuffleImages = (question) => {
  if (!question || !currentGroup.value.imageRange) return

  const {start, end} = currentGroup.value.imageRange;
  let selectedImages = [];
  const allImages = Array.from({length: end - start + 1}, (_, i) => start + i); // 生成从start到end的数组

  while (selectedImages.length < 4 && allImages.length > 0) {
    const randomIndex = Math.floor(Math.random() * allImages.length);
    const chosenNumber = allImages[randomIndex];
    selectedImages.push(chosenNumber);
    allImages.splice(randomIndex, 1); // 移除已选中的图片避免重复
  }

  question.options = selectedImages.map((imgNum, index) => ({
    label: `选项 ${index + 1}`,
    value: `${imgNum}.jpg`,
    image: `${currentGroup.value.imagesPath}${imgNum}.jpg`
  }));
};

// 监听当前问题变化
watch(currentQuestion, (newVal) => {
  if (newVal?.type === 'image-single' && newVal.options && newVal.options.length === 0) {
    shuffleImages(newVal); // 当切换到新问题时自动加载一组图片
  }
});
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease-out forwards;
}

.animate-slideUp {
  animation: slideUp 0.5s ease-out forwards;
}
</style>