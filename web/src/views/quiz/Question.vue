<template>
  <AppHeader />
  <div class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          疗愈香氛偏好测试
        </h1>
        <div class="flex items-center justify-between mb-6">
            <div class="text-lg font-medium text-gray-700">
              第 {{ currentPart }} 部分 / 共 4 部分
            </div>
            <div class="text-sm text-gray-500">
              第 {{ (visibleQuestionIndex || 0) + 1 }} 题 / 共 {{ totalVisibleQuestions }} 题
            </div>
          </div>
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
          <button
              v-if="currentQuestion.type === 'image-multiple' && currentQuestion.id === 'q4'"
              @click="refreshFragranceImages"
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
              v-if="(visibleQuestionIndex || 0) > 0"
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
            {{ loading ? '处理中...' : (visibleQuestionIndex === ((visibleQuestions && visibleQuestions.length) ? visibleQuestions.length - 1 : 0) ? (currentPart.value === 4 ? '完成测试' : '下一部分 →') : '下一题 →') }}
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
import {useRoute, useRouter} from 'vue-router'
import {getQuestionGroups, createQuizSession, saveUserAnswer, completeQuizSession, resumeIncompleteSession, getPhasedQuestions, checkIncompleteSession, getFragranceImages, submitPart} from '@/api/quiz.api.js'
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

// ===== 响应式状态 =====
const sessionId = ref('')
const startTime = ref(Date.now())
const answers = ref({})
const currentVisibleIndex = ref(0)
const tempAnswer = ref('')
const tempMultiAnswer = ref([])
const tempTextAnswer = ref('')
const loading = ref(false)
const error = ref('')
const completed = ref(false)
const loadedSessionData = ref(null)
const allQuestionsWithGroup = ref([])
const visibleQuestions = ref([])
const currentPart = ref(1) // 当前部分，初始为1
const completedParts = ref([]) // 已完成的部分列表
const fragranceImageQuestion = ref(null)

// 路由
const route = useRoute()

onMounted(() => {
  // 检查URL参数中是否有new=true，如果有则强制创建新会话
  const forceNew = route.query.new === 'true'
  // 确保使用URL中的sessionId
  const urlSessionId = route.query.sessionId
  if (urlSessionId) {
    sessionId.value = urlSessionId
  }
  initQuestions(forceNew)
})

const initQuestions = async (forceNew = false) => {
  loading.value = true
  error.value = ''
  
  try {
    // 检查URL参数
    const route = useRoute()
    const urlSessionId = route.query.sessionId
    const isNew = route.query.new === 'true' || forceNew
    
    console.log('🔍 初始化题目，参数:', { urlSessionId, isNew, forceNew })
    
    if (urlSessionId && !isNew) {
      // 如果有sessionId且不是强制新建，则尝试恢复会话
      sessionId.value = urlSessionId
      console.log('🔄 尝试恢复会话:', sessionId.value)
      
      try {
        const result = await resumeIncompleteSession(sessionId.value)
        loadedSessionData.value = result.session
        answers.value = result.answers
        
        // 确定当前部分
        currentPart.value = result.session.current_part || 1
        
        // 标记已完成的部分
        completedParts.value = []
        for (let i = 1; i < currentPart.value; i++) {
          completedParts.value.push(i)
        }
        
        console.log('✅ 会话恢复成功:', {
          sessionId: sessionId.value,
          currentPart: currentPart.value,
          completedParts: completedParts.value
        })
        
        // 加载当前部分的题目
        const response = await getPhasedQuestions(currentPart.value, sessionId.value)
        const groupData = response.data
        
        // 构建题目序列
        allQuestionsWithGroup.value = []
        
        // 处理题目数据
        if (groupData.questions && Array.isArray(groupData.questions)) {
          groupData.questions.forEach(q => {
            // 优先使用数据库中的max_selection字段，兼容maxSelection
            const calculatedMaxSelection = q.max_selection || q.maxSelection;
            
            allQuestionsWithGroup.value.push({
              id: q.id,
              groupId: groupData.id,
              groupTitle: groupData.title,
              groupDescription: groupData.description,
              imageRange: q.image_range || 1,
              imagesPath: q.images_path || '',
              text: q.text,
              type: q.type,
              options: q.options || [],
              minSelection: q.min_selection || 1,
              maxSelection: calculatedMaxSelection,
              showTextWhen: q.showText_when,
              condition: q.condition
            })
          })
          
          // 如果是第四部分，保存主香调和次香调信息到题目数据中
          if (currentPart.value === 4) {
            // 将主香调和次香调信息添加到每个题目中
            allQuestionsWithGroup.value.forEach(q => {
              q.mainFragrance = groupData.mainFragrance;
              q.secondaryFragrance = groupData.secondaryFragrance;
              q.main_images = groupData.main_images;
              q.secondary_images = groupData.secondary_images;
            });
          }
        }
        
        // 更新可见题目列表
        updateVisibleQuestions()
        
        // 如果会话数据，尝试找到最后回答的题目位置
        if (Object.keys(answers.value).length > 0) {
          // 找到最后回答的题目
          let answeredQuestions = Object.keys(answers.value)
          console.log('已回答的题目ID:', answeredQuestions)
          
          // 获取最后一个回答的题目ID
          const lastAnsweredQuestionId = answeredQuestions[answeredQuestions.length - 1]
          console.log('最后回答的题目ID:', lastAnsweredQuestionId)
          
          // 找到最后回答的题目在当前部分可见题目中的索引
          let lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === lastAnsweredQuestionId)
          console.log('最后回答的题目在可见题目中的索引:', lastAnsweredIndex)
          
          // 如果找不到匹配的题目ID，检查是否是特殊格式（如"q3"、"q4"）
          if (lastAnsweredIndex === -1 && (lastAnsweredQuestionId === 'q3' || lastAnsweredQuestionId === 'q4')) {
            console.log(`⚠️ 未找到题目ID ${lastAnsweredQuestionId}，可能是特殊格式，尝试查找匹配的题目`)
            
            // 对于"q3"，查找第3部分的第一个题目
            if (lastAnsweredQuestionId === 'q3' && currentPart.value === 3) {
              // 查找第3部分的第一个题目
              const part3Question = visibleQuestions.value.find(q => q.id.startsWith('q3-'))
              if (part3Question) {
                lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === part3Question.id)
                console.log(`✅ 找到第3部分的第一个题目: ${part3Question.id}，索引: ${lastAnsweredIndex}`)
              }
            }
            
            // 对于"q4"，查找第4部分的第一个题目
            if (lastAnsweredQuestionId === 'q4' && currentPart.value === 4) {
              // 查找第4部分的第一个题目
              const part4Question = visibleQuestions.value.find(q => q.id.startsWith('q4-'))
              if (part4Question) {
                lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === part4Question.id)
                console.log(`✅ 找到第4部分的第一个题目: ${part4Question.id}，索引: ${lastAnsweredIndex}`)
              }
            }
          }
          
          // 如果仍然找不到匹配的题目，尝试使用部分编号和题目编号来匹配
          if (lastAnsweredIndex === -1) {
            console.log(`⚠️ 仍然未找到题目ID ${lastAnsweredQuestionId}，尝试使用部分编号和题目编号匹配`)
            
            // 提取部分编号和题目编号
            const partMatch = lastAnsweredQuestionId.match(/q(\d+)-?(\d*)/)
            if (partMatch) {
              const partNum = parseInt(partMatch[1])
              const questionNum = partMatch[2] ? parseInt(partMatch[2]) : 1
              
              console.log(`提取部分编号: ${partNum}, 题目编号: ${questionNum}`)
              
              // 如果部分编号匹配当前部分，尝试找到对应题目
              if (partNum === targetPart) {
                // 查找匹配的题目
                const targetQuestion = visibleQuestions.value.find(q => {
                  const qMatch = q.id.match(/q(\d+)-?(\d*)/)
                  if (qMatch) {
                    const qPartNum = parseInt(qMatch[1])
                    const qQuestionNum = qMatch[2] ? parseInt(qMatch[2]) : 1
                    return qPartNum === partNum && qQuestionNum === questionNum
                  }
                  return false
                })
                
                if (targetQuestion) {
                  lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === targetQuestion.id)
                  console.log(`✅ 通过部分和题目编号找到匹配题目: ${targetQuestion.id}，索引: ${lastAnsweredIndex}`)
                }
              }
            }
          }
          
          if (lastAnsweredIndex !== -1) {
            // 如果找到已回答的题目，检查是否是当前部分的最后一题
            if (lastAnsweredIndex === visibleQuestions.value.length - 1) {
              // 如果是最后一题，保持在这个位置
              currentVisibleIndex.value = lastAnsweredIndex
              console.log('✅ 定位到当前部分最后一题:', currentVisibleIndex.value + 1)
            } else {
              // 如果不是最后一题，跳转到下一题
              currentVisibleIndex.value = lastAnsweredIndex + 1
              console.log('✅ 定位到未完成题目位置:', currentVisibleIndex.value + 1)
            }
            // 确保加载对应的题目状态
            setTimeout(() => loadCurrentQuestionState(), 100)
          } else {
            // 如果在当前部分没有找到最后回答的题目，可能是因为题目ID格式不匹配
            // 这种情况下，我们跳转到当前部分的第一题
            currentVisibleIndex.value = 0
            console.log('⚠️ 未在当前部分找到最后回答的题目，跳转到第一题')
          }
        } else {
          // 如果没有已回答的题目，跳转到第一题
          currentVisibleIndex.value = 0
          console.log('📝 没有已回答的题目，跳转到第一题')
        }
        
        return
      } catch (err) {
        console.error('恢复会话失败:', err)
        // 恢复失败时继续正常流程
      }
    }
    
    // 如果强制创建新会话，清除所有会话数据
    if (forceNew) {
      console.log('🔄 强制创建新会话，清除所有会话数据')
      sessionId.value = ''
      answers.value = {}
      loadedSessionData.value = null
      completedParts.value = []
      currentPart.value = 1
      localStorage.removeItem('currentQuizSession')
    }
    
    // 如果不是强制创建新会话且没有初始会话数据，检查是否有未完成的会话
    if (!forceNew && !props.initialSession && !loadedSessionData.value) {
      try {
        const incompleteSession = await checkIncompleteSession()
        if (incompleteSession.data && incompleteSession.data.session_id) {
          // 如果有未完成的会话，恢复它
          const sessionData = await resumeIncompleteSession(incompleteSession.data.session_id)
          loadedSessionData.value = sessionData.session
          sessionId.value = sessionData.session.session_id
          startTime.value = sessionData.session.start_time ? new Date(sessionData.session.start_time).getTime() : Date.now()
          
          // 加载答案数据
          if (sessionData.answers && typeof sessionData.answers === 'object') {
            console.log('📥 从未完成会话加载答案数据:', sessionData.answers)
            answers.value = {...sessionData.answers}
          }
          
          // 验证答案数据是否正确加载
          if (Object.keys(answers.value).length > 0) {
            console.log('✅ 恢复会话成功，已加载答案数:', Object.keys(answers.value).length)
            console.log('✅ 当前会话ID:', sessionId.value)
          } else {
            console.log('⚠️ 未加载到任何答案数据')
          }
        }
      } catch (err) {
        console.warn('检查未完成会话失败:', err)
      }
    }
    
    // 检查是否有初始会话数据或从本地存储加载的会话数据
    if (!forceNew && ((props.initialSession && props.initialSession.session_id) || loadedSessionData.value)) {
      // console.log('✅ 检测到会话数据，准备恢复')
      // 使用之前的会话ID
      const sessionData = props.initialSession || loadedSessionData.value
      
      // 确保answers.value初始化为空对象
      if (!answers.value || Object.keys(answers.value).length === 0) {
        answers.value = {};
      }
      
      // 检查数据格式，确保正确提取数据
      if (sessionData.session) {
        // console.log('📋 使用resumeIncompleteSession返回的格式')
        // 这是从resumeIncompleteSession返回的格式
        sessionId.value = sessionData.session.session_id
        startTime.value = sessionData.session.start_time ? new Date(sessionData.session.start_time).getTime() : Date.now()
        
        // 正确处理answerMap格式的答案数据
        if (sessionData.answers && typeof sessionData.answers === 'object' && Object.keys(sessionData.answers).length > 0) {
          // console.log('📥 加载答案数据:', sessionData.answers)
          // 检查是否是数组格式，如果是则转换为对象格式
          if (Array.isArray(sessionData.answers)) {
            console.log('⚠️ 检测到sessionData.answers是数组格式，正在转换为对象格式')
            const answersObj = {}
            sessionData.answers.forEach((answer, index) => {
              // 如果数组元素有question_id属性，使用它作为键
              if (answer.question_id) {
                answersObj[answer.question_id] = answer.value || answer
              } else {
                // 否则使用索引作为键，假设是q1-1, q1-2等格式
                answersObj[`q1-${index + 1}`] = answer
              }
            })
            answers.value = answersObj
            console.log('✅ 转换后的answers.value:', answers.value)
          } else {
            answers.value = {...sessionData.answers}
          }
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
          // 检查是否是数组格式，如果是则转换为对象格式
          if (Array.isArray(sessionData.answers)) {
            console.log('⚠️ 检测到sessionData.answers是数组格式，正在转换为对象格式')
            const answersObj = {}
            sessionData.answers.forEach((answer, index) => {
              // 如果数组元素有question_id属性，使用它作为键
              if (answer.question_id) {
                answersObj[answer.question_id] = answer.value || answer
              } else {
                // 否则使用索引作为键，假设是q1-1, q1-2等格式
                answersObj[`q1-${index + 1}`] = answer
              }
            })
            answers.value = answersObj
            console.log('✅ 转换后的answers.value:', answers.value)
          } else {
            answers.value = {...sessionData.answers}
          }
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
      
      // 根据已回答的题目数量确定应该加载哪个部分
      let partToLoad = 1
      const answeredCount = Object.keys(answers.value).length
      if (answeredCount >= 20) {
        partToLoad = 4 // 直接加载第4部分（香调图片题目）
        completedParts.value = [1, 2, 3] // 假设前3部分已完成
      }
      
      // 设置当前部分
      currentPart.value = partToLoad
      
      // 分阶段获取题目数据
      const response = await getPhasedQuestions(partToLoad, sessionId.value)
      const groupData = response.data
      
      // 构建题目序列
      allQuestionsWithGroup.value = []
      
      // 处理题目数据
            if (groupData.questions && Array.isArray(groupData.questions)) {
              groupData.questions.forEach(q => {
                // 优先使用数据库中的max_selection字段，兼容maxSelection
                const calculatedMaxSelection = q.max_selection || q.maxSelection;
                
                allQuestionsWithGroup.value.push({
                  id: q.id,
                  groupId: groupData.id,
                  groupTitle: groupData.title,
                  groupDescription: groupData.description,
                  imageRange: q.image_range || 1,
                  imagesPath: q.images_path || '',
                  text: q.text,
                  type: q.type,
                  options: q.options || [],
                  minSelection: q.min_selection || 1,
                  maxSelection: calculatedMaxSelection,
                  showTextWhen: q.showText_when,
                  condition: q.condition,
                  // 添加主香调和次香调字段
                  mainFragrance: groupData.mainFragrance,
                  secondaryFragrance: groupData.secondaryFragrance
                })
              })
        
        // 如果是第四部分，保存主香调和次香调信息
        if (currentPart.value === 4) {
          // 保存主香调和次香调信息
          if (groupData.mainFragrance) {
            currentGroup.value.mainFragrance = groupData.mainFragrance;
          }
          if (groupData.secondaryFragrance) {
            currentGroup.value.secondaryFragrance = groupData.secondaryFragrance;
          }
        }
      }
      
      // 如果是第4部分（香调图片题目），标记前20题已提交
      if (partToLoad === 4) {
        // 不再需要isFirst20Submitted标记，直接进入第4部分
      }
    } else {
      // 创建新的测验会话
      try {
        const sessionData = await createQuizSession()
        sessionId.value = sessionData.session_id
        console.log('✅ 创建新会话成功，会话ID:', sessionId.value)
      } catch (sessionError) {
        console.warn('创建会话失败，使用临时会话ID:', sessionError)
        // 生成临时会话ID，确保功能可以继续使用
        sessionId.value = 'TEMP_' + Date.now()
      }
      
      // 获取第一部分题目
      const response = await getPhasedQuestions(1)
      const groupData = response.data
      
      // 构建题目序列
      allQuestionsWithGroup.value = []
      
      // 处理题目数据
      if (groupData.questions && Array.isArray(groupData.questions)) {
        groupData.questions.forEach(q => {
          // 优先使用数据库中的max_selection字段，兼容maxSelection
          const calculatedMaxSelection = q.max_selection || q.maxSelection;
          
          allQuestionsWithGroup.value.push({
            id: q.id,
            groupId: groupData.id,
            groupTitle: groupData.title,
            groupDescription: groupData.description,
            imageRange: q.image_range || 1,
            imagesPath: q.images_path || '',
            text: q.text,
            type: q.type,
            options: q.options || [],
            minSelection: q.min_selection || 1,
            maxSelection: calculatedMaxSelection,
            showTextWhen: q.showText_when,
            condition: q.condition
          })
        })
      }
    }
    
    // 初始化可见题目
    updateVisibleQuestions()
    
    // 如果会话数据，尝试找到最后回答的题目位置
    if (Object.keys(answers.value).length > 0) {
      // 找到最后回答的题目
      // 注意：answers.value的结构应该是 {q1-1: {value: 'D'}, q1-2: {value: 'E'}, ...}
      // 所以Object.keys(answers.value)返回的是实际的题目ID，如['q1-1', 'q1-2', ...]
      let answeredQuestions
      
      // 检查answers.value是否是数组格式，如果是，需要转换为对象格式
      if (Array.isArray(answers.value)) {
        console.log('⚠️ 检测到answers.value是数组格式，正在转换为对象格式')
        const answersObj = {}
        answers.value.forEach((answer, index) => {
          // 如果数组元素有question_id属性，使用它作为键
          if (answer.question_id) {
            answersObj[answer.question_id] = answer.value || answer
          } else {
            // 否则使用索引作为键，假设是q1-1, q1-2等格式
            answersObj[`q1-${index + 1}`] = answer
          }
        })
        answers.value = answersObj
        console.log('✅ 转换后的answers.value:', answers.value)
      }
      
      answeredQuestions = Object.keys(answers.value)
      console.log('已回答的题目ID:', answeredQuestions)
      
      // 获取最后一个回答的题目ID
      const lastAnsweredQuestionId = answeredQuestions[answeredQuestions.length - 1]
      console.log('最后回答的题目ID:', lastAnsweredQuestionId)
      
      // 根据题目ID判断它属于哪个部分
      // 题目ID格式为"q1-1"、"q2-1"、"q3-1"、"q4-1"等，或者是"q3"、"q4"等格式
      let targetPart = 1
      
      if (lastAnsweredQuestionId.startsWith('q4-') || lastAnsweredQuestionId === 'q4') {
        targetPart = 4 // 第4部分：香调图片题目
      } else if (lastAnsweredQuestionId.startsWith('q3-') || lastAnsweredQuestionId === 'q3') {
        targetPart = 3 // 第3部分：情境题目
      } else if (lastAnsweredQuestionId.startsWith('q2-') || lastAnsweredQuestionId === 'q2') {
        targetPart = 2 // 第2部分：多选题目
      } else if (lastAnsweredQuestionId.startsWith('q1-') || lastAnsweredQuestionId === 'q1') {
        targetPart = 1 // 第1部分：单选题目
      }
      
      console.log('根据题目ID判断目标部分:', targetPart)
      
      // 如果当前部分不是目标部分，需要切换到目标部分
      if (currentPart.value !== targetPart) {
        console.log(`从第${currentPart.value}部分切换到第${targetPart}部分`)
        
        // 更新当前部分和已完成部分
        currentPart.value = targetPart
        
        // 根据目标部分设置已完成部分
        if (targetPart === 4) {
          completedParts.value = [1, 2, 3]
        } else if (targetPart === 3) {
          completedParts.value = [1, 2]
        } else if (targetPart === 2) {
          completedParts.value = [1]
        }
        
        // 重新加载目标部分的题目
        const response = await getPhasedQuestions(targetPart, sessionId.value)
        const groupData = response.data
        
        // 构建题目序列
        allQuestionsWithGroup.value = []
        if (groupData.questions && Array.isArray(groupData.questions)) {
          groupData.questions.forEach(q => {
            const calculatedMaxSelection = q.max_selection || q.maxSelection;
            allQuestionsWithGroup.value.push({
              id: q.id,
              groupId: groupData.id,
              groupTitle: groupData.title,
              groupDescription: groupData.description,
              imageRange: q.image_range || 1,
              imagesPath: q.images_path || '',
              text: q.text,
              type: q.type,
              options: q.options || [],
              minSelection: q.min_selection || 1,
              maxSelection: calculatedMaxSelection,
              showTextWhen: q.showText_when,
              condition: q.condition
            })
          })
        }
        
        // 更新可见题目列表
        updateVisibleQuestions()
      }
      
      // 找到最后回答的题目在当前部分可见题目中的索引
      let lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === lastAnsweredQuestionId)
      console.log('最后回答的题目在可见题目中的索引:', lastAnsweredIndex)
      
      // 如果找不到匹配的题目ID，检查是否是特殊格式（如"q3"、"q4"）
      if (lastAnsweredIndex === -1 && (lastAnsweredQuestionId === 'q3' || lastAnsweredQuestionId === 'q4')) {
        console.log(`⚠️ 未找到题目ID ${lastAnsweredQuestionId}，可能是特殊格式，尝试查找匹配的题目`)
        
        // 对于"q3"，查找第3部分的第一个题目
        if (lastAnsweredQuestionId === 'q3' && targetPart === 3) {
          // 查找第3部分的第一个题目
          const part3Question = visibleQuestions.value.find(q => q.id.startsWith('q3-'))
          if (part3Question) {
            lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === part3Question.id)
            console.log(`✅ 找到第3部分的第一个题目: ${part3Question.id}，索引: ${lastAnsweredIndex}`)
          }
        }
        
        // 对于"q4"，查找第4部分的第一个题目
        if (lastAnsweredQuestionId === 'q4' && targetPart === 4) {
          // 查找第4部分的第一个题目
          const part4Question = visibleQuestions.value.find(q => q.id.startsWith('q4-'))
          if (part4Question) {
            lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === part4Question.id)
            console.log(`✅ 找到第4部分的第一个题目: ${part4Question.id}，索引: ${lastAnsweredIndex}`)
          }
        }
      }
      
      // 如果仍然找不到匹配的题目，尝试使用部分编号和题目编号来匹配
      if (lastAnsweredIndex === -1) {
        console.log(`⚠️ 仍然未找到题目ID ${lastAnsweredQuestionId}，尝试使用部分编号和题目编号匹配`)
        
        // 提取部分编号和题目编号
        const partMatch = lastAnsweredQuestionId.match(/q(\d+)-?(\d*)/)
        if (partMatch) {
          const partNum = parseInt(partMatch[1])
          const questionNum = partMatch[2] ? parseInt(partMatch[2]) : 1
          
          console.log(`提取部分编号: ${partNum}, 题目编号: ${questionNum}`)
          
          // 如果部分编号匹配当前部分，尝试找到对应题目
          if (partNum === targetPart) {
            // 查找匹配的题目
            const targetQuestion = visibleQuestions.value.find(q => {
              const qMatch = q.id.match(/q(\d+)-?(\d*)/)
              if (qMatch) {
                const qPartNum = parseInt(qMatch[1])
                const qQuestionNum = qMatch[2] ? parseInt(qMatch[2]) : 1
                return qPartNum === partNum && qQuestionNum === questionNum
              }
              return false
            })
            
            if (targetQuestion) {
              lastAnsweredIndex = visibleQuestions.value.findIndex(q => q.id === targetQuestion.id)
              console.log(`✅ 通过部分和题目编号找到匹配题目: ${targetQuestion.id}，索引: ${lastAnsweredIndex}`)
            }
          }
        }
      }
      
      if (lastAnsweredIndex !== -1) {
        // 如果找到已回答的题目，检查是否是当前部分的最后一题
        if (lastAnsweredIndex === visibleQuestions.value.length - 1) {
          // 如果是最后一题，保持在这个位置
          currentVisibleIndex.value = lastAnsweredIndex
          console.log('✅ 定位到当前部分最后一题:', currentVisibleIndex.value + 1)
        } else {
          // 如果不是最后一题，跳转到下一题
          currentVisibleIndex.value = lastAnsweredIndex + 1
          console.log('✅ 定位到未完成题目位置:', currentVisibleIndex.value + 1)
        }
        // 确保加载对应的题目状态
        setTimeout(() => loadCurrentQuestionState(), 100)
      } else {
        // 如果在当前部分没有找到最后回答的题目，可能是因为题目ID格式不匹配
        // 这种情况下，我们跳转到当前部分的第一题
        currentVisibleIndex.value = 0
        console.log('⚠️ 未在当前部分找到最后回答的题目，跳转到第一题')
      }
    } else {
      // 如果没有已回答的题目，跳转到第一题
      currentVisibleIndex.value = 0
      console.log('📝 没有已回答的题目，跳转到第一题')
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
  if (allQuestionsWithGroup.value) {
    for (const q of allQuestionsWithGroup.value) {
      if (!q.condition || q.condition(answers.value)) {
        result.push(q)
      }
    }
  }
  
  visibleQuestions.value = result
  if (visibleQuestions.value && currentVisibleIndex.value >= visibleQuestions.value.length && visibleQuestions.value.length > 0) {
    currentVisibleIndex.value = visibleQuestions.value.length - 1
  }
  // 只有在有可见题目时才加载当前题目状态
  if (visibleQuestions.value && visibleQuestions.value.length > 0) {
    loadCurrentQuestionState()
  }
}

watch(answers, () => updateVisibleQuestions(), {deep: true})

// ===== 计算属性 =====
const currentQuestion = computed(() => {
  if (!visibleQuestions.value || !visibleQuestions.value.length || currentVisibleIndex.value === undefined || currentVisibleIndex.value < 0 || currentVisibleIndex.value >= visibleQuestions.value.length) {
    return null
  }
  return visibleQuestions.value[currentVisibleIndex.value]
})
const currentGroup = computed(() => currentQuestion.value ? {
  title: currentQuestion.value.groupTitle,
  description: currentQuestion.value.groupDescription,
  imageRange: currentQuestion.value.imageRange,
  imagesPath: currentQuestion.value.imagesPath,
  mainFragrance: currentQuestion.value.mainFragrance,
  secondaryFragrance: currentQuestion.value.secondaryFragrance,
  main_images: currentQuestion.value.main_images,
  secondary_images: currentQuestion.value.secondary_images
} : {})

const visibleQuestionIndex = computed(() => currentVisibleIndex.value)
const totalVisibleQuestions = computed(() => visibleQuestions.value ? visibleQuestions.value.length : 0)

const isAnswered = computed(() => {
  const q = currentQuestion.value
  if (!q) return false

  if (q.type === 'single' || q.type === 'image-single') {
    return !!tempAnswer.value
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    return tempMultiAnswer.value && tempMultiAnswer.value.length >= (q.minSelection || 1) &&
        tempMultiAnswer.value.length <= (q.maxSelection || Infinity)
  } else if (q.type === 'single-with-text') {
    if (!tempAnswer.value) return false
    if (tempAnswer.value === q.showTextWhen) {
      return !!tempTextAnswer.value && (typeof tempTextAnswer.value === 'string' ? tempTextAnswer.value.trim() : tempTextAnswer.value)
    }
    return true
  } else if (q.type === 'text') {
    return !!tempTextAnswer.value && (typeof tempTextAnswer.value === 'string' ? tempTextAnswer.value.trim() : tempTextAnswer.value)
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
  if (!q) {
    console.log('当前题目为空，跳过加载题目状态')
    return
  }

  // showTextWhen属性的处理现在在SingleWithText.vue组件内部进行，避免直接修改props

  // 打乱选择题选项顺序
  if (q.options && Array.isArray(q.options) && 
      (q.type === 'single' || q.type === 'multiple' || q.type === 'single-with-text')) {
    // 为了保持答案一致性，我们在打乱前创建一个副本
    q.shuffledOptions = shuffleArray([...q.options])
  }

  const saved = answers.value[q.id]
  console.log(`📋 加载题目 ${q.id} 的状态，保存的答案数据:`, saved)
  
  // 处理可能的JSON字符串格式
  let parsedSaved = saved
  if (typeof saved === 'string') {
    try {
      parsedSaved = JSON.parse(saved)
      console.log(`🔄 解析JSON字符串格式的答案:`, parsedSaved)
    } catch (e) {
      // 检查是否是纯文本格式的答案（不包含JSON结构）
      const isPlainText = typeof saved === 'string' && 
                         !saved.trim().startsWith('{') && 
                         !saved.trim().startsWith('[')
      
      if (isPlainText) {
        // 对于纯文本格式的答案，不显示错误信息
        console.log(`ℹ️ 题目 ${q.id} 的答案数据为纯文本格式`)
      } else {
        // 对于可能是JSON但格式错误的答案，只在开发环境下显示详细错误信息
        if (process.env.NODE_ENV === 'development') {
          console.warn(`⚠️ 无法解析题目 ${q.id} 的答案JSON字符串:`, e)
        } else {
          console.log(`ℹ️ 题目 ${q.id} 的答案数据格式可能有误`)
        }
      }
      parsedSaved = saved
    }
  }
  
  if (q.type === 'single' || q.type === 'image-single') {
    tempAnswer.value = parsedSaved?.value || ''
    console.log(`✅ 单选题 ${q.id} 设置答案为:`, tempAnswer.value)
  } else if (q.type === 'multiple' || q.type === 'image-multiple') {
    // 处理字符串格式的数组或普通数组
    if (Array.isArray(parsedSaved)) {
      tempMultiAnswer.value = [...parsedSaved]
    } else if (typeof parsedSaved === 'string') {
      try {
        // 尝试解析字符串格式的数组
        const parsed = JSON.parse(parsedSaved)
        tempMultiAnswer.value = Array.isArray(parsed) ? [...parsed] : []
      } catch {
        tempMultiAnswer.value = []
      }
    } else {
      tempMultiAnswer.value = []
    }
    console.log(`✅ 多选题 ${q.id} 设置答案为:`, tempMultiAnswer.value)
  } else if (q.type === 'single-with-text') {
    if (parsedSaved && typeof parsedSaved === 'object') {
      tempAnswer.value = parsedSaved.value || ''
      tempTextAnswer.value = parsedSaved.text || ''
    } else {
      tempAnswer.value = ''
      tempTextAnswer.value = ''
    }
    console.log(`✅ 带文本单选题 ${q.id} 设置答案为:`, { value: tempAnswer.value, text: tempTextAnswer.value })
  } else if (q.type === 'text') {
    // 对于纯文本类型题目，处理可能的JSON嵌套字符串
    if (typeof parsedSaved === 'string') {
      try {
        // 尝试解析可能嵌套的JSON字符串
        const parsed = JSON.parse(parsedSaved);
        // 如果解析结果是对象，尝试获取其value或text属性
        if (typeof parsed === 'object') {
          tempTextAnswer.value = String(parsed.value || parsed.text || '');
        } else {
          // 否则使用解析后的值，并转换为字符串
          tempTextAnswer.value = String(parsed || '');
        }
      } catch (e) {
        // 如果解析失败，使用原始字符串
        tempTextAnswer.value = parsedSaved;
      }
    } else if (parsedSaved && typeof parsedSaved === 'object') {
      // 如果parsedSaved是对象，尝试获取其value或text属性，并转换为字符串
      tempTextAnswer.value = String(parsedSaved.value || parsedSaved.text || '');
    } else {
      // 对于其他类型（数字、布尔值等），转换为字符串
      tempTextAnswer.value = String(parsedSaved || '');
    }
    console.log(`✅ 文本题 ${q.id} 设置答案为:`, tempTextAnswer.value)
  }
}

const saveAnswer = async () => {
  const q = currentQuestion.value
  if (!q || !sessionId.value) return

  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  const effectiveSessionId = urlSessionId || sessionId.value;

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
    await saveUserAnswer(effectiveSessionId, q.id, answerData)
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

    // 检查是否是当前部分的最后一题
    if (visibleQuestions.value && currentVisibleIndex.value === visibleQuestions.value.length - 1) {
      // 标记当前部分已完成
      if (!completedParts.value.includes(currentPart.value)) {
        completedParts.value.push(currentPart.value)
      }
      
      // 确保使用当前URL中的sessionId
      const currentUrl = new URL(window.location.href);
      const urlSessionId = currentUrl.searchParams.get('sessionId');
      const effectiveSessionId = urlSessionId || sessionId.value;
      
      // 提交当前部分，更新后端的current_part
      try {
        await submitPart(effectiveSessionId, currentPart.value, answers.value)
      } catch (err) {
        console.error('提交部分失败:', err)
        // 即使提交失败，也继续流程，只是current_part可能不会更新
      }
      
      // 检查是否已完成所有部分
      if (completedParts.value.length >= 4) {
        // 完成测验
        await completeQuizSession(effectiveSessionId)
        completed.value = true
        emit('complete', getReport())
      } else {
        // 加载下一部分
        let nextPart = currentPart.value + 1
        
        // 特殊处理第3部分完成后设置默认香调信息
        if (currentPart.value === 3 && nextPart === 4) {
          // 直接设置默认香调信息
          currentGroup.value.mainFragrance = "柑橘类";
          currentGroup.value.secondaryFragrance = "蔬果类";
        }
        
        
        
        // 跳过已加载的部分
        while (nextPart <= 4 && completedParts.value.includes(nextPart)) {
          nextPart++
        }
        
        if (nextPart <= 4) {
          // 加载下一部分题目
          currentPart.value = nextPart
          // 确保使用当前URL中的sessionId
          const response = await getPhasedQuestions(nextPart, effectiveSessionId)
          const groupData = response.data
          
          // 构建题目序列
          allQuestionsWithGroup.value = []
          
          // 处理题目数据
          if (groupData.questions && Array.isArray(groupData.questions)) {
            groupData.questions.forEach(q => {
              // 优先使用数据库中的max_selection字段，兼容maxSelection
              const calculatedMaxSelection = q.max_selection || q.maxSelection;
              
              allQuestionsWithGroup.value.push({
                id: q.id,
                groupId: groupData.id,
                groupTitle: groupData.title,
                groupDescription: groupData.description,
                imageRange: q.image_range || 1,
                imagesPath: q.images_path || '',
                text: q.text,
                type: q.type,
                options: q.options || [],
                minSelection: q.min_selection || 1,
                maxSelection: calculatedMaxSelection,
                showTextWhen: q.showText_when,
                condition: q.condition
              })
            })
            
            // 如果是第四部分，保存主香调和次香调信息到题目数据中
            if (currentPart.value === 4) {
              // 将主香调和次香调信息添加到每个题目中
              allQuestionsWithGroup.value.forEach(q => {
                q.mainFragrance = groupData.mainFragrance;
                q.secondaryFragrance = groupData.secondaryFragrance;
                q.main_images = groupData.main_images;
                q.secondary_images = groupData.secondary_images;
              });
            }
          }
          
          // 更新可见题目列表
          updateVisibleQuestions()
          
          // 重置到第一题
          currentVisibleIndex.value = 0
        } else {
          // 如果没有更多部分，完成测验
          await completeQuizSession(sessionId.value)
          completed.value = true
          emit('complete', getReport())
        }
      }
    } else {
      // 当前部分内移动到下一题
      currentVisibleIndex.value++
    }
    
    // 加载当前题目的状态
    setTimeout(() => {
      if (visibleQuestions.value && visibleQuestions.value.length > 0) {
        loadCurrentQuestionState()
      }
    }, 50)
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
    // 只有在有可见题目时才调用`loadCurrentQuestionState`：
    if (visibleQuestions.value && visibleQuestions.value.length > 0) {
      loadCurrentQuestionState()
    }
  } catch (err) {
    console.error('处理上一题失败:', err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  // 检查是否已完成所有部分
  if (completedParts.value.length < 4) {
    alert(`请完成所有部分后再提交问卷。当前已完成 ${completedParts.value.length}/4 部分。`)
    return
  }
  
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  const effectiveSessionId = urlSessionId || sessionId.value;
  
  const report = getReport()
  console.log('📝 提交报告:', report)
  
  try {
    // 确保测验已经完成
    if (!completed.value && effectiveSessionId) {
      await completeQuizSession(effectiveSessionId)
    }
    alert('感谢参与！你的专属香氛报告已生成并保存。')
  } catch (err) {
    console.error('提交报告失败:', err)
    alert('保存报告失败，请稍后重试。')
  }
}

const handleRestart = () => {
  // 跳转到带有new=true参数的URL，强制创建新会话
  const router = useRouter()
  router.push({
    path: '/quiz/question',
    query: { new: 'true' }
  })
}

const reset = (forceNew = false) => {
  answers.value = {}
  completed.value = false
  startTime.value = Date.now()
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  sessionId.value = urlSessionId || ''
  currentVisibleIndex.value = 0
  tempAnswer.value = ''
  tempMultiAnswer.value = []
  tempTextAnswer.value = ''
  error.value = ''
  currentPart.value = 1 // 重置为第一部分
  completedParts.value = [] // 清空已完成部分列表
  initQuestions(forceNew)
}

defineExpose({
  reset
})

const getReport = () => {
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  const effectiveSessionId = urlSessionId || sessionId.value;
  
  return {
    id: effectiveSessionId || 'AROMA_' + Date.now(),
    startTime: new Date(startTime.value).toISOString(),
    endTime: new Date().toISOString(),
    durationMs: Date.now() - startTime.value,
    answers: {...answers.value},
    completedAt: new Date().toLocaleString(),
    // 如果是继续的会话，包含原始开始时间
    originalStartTime: loadedSessionData.value?.start_time || null
  }
}

// 方法定义
const shuffleImages = (question) => {
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  
  if (!question || !currentGroup.value || !currentGroup.value.imageRange) return

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
    image: `${currentGroup.value.imagesPath || ''}${imgNum}.jpg`
  }));
};

// 新增函数：处理第四部分图片选项
const shuffleFragranceImages = async (question) => {
  if (!question || question.id !== 'q4') return;
  
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  
  // 获取主香调和次香调，不设置默认值，完全按照后端返回的信息
  const mainFragrance = currentGroup.value.mainFragrance;
  const secondaryFragrance = currentGroup.value.secondaryFragrance;
  
  // 检查是否获取到了主香调和次香调
  if (!mainFragrance || !secondaryFragrance) {
    console.error('未能获取到主香调或次香调信息:', { mainFragrance, secondaryFragrance });
    // 使用空数组作为选项，不设置默认图片
    question.options = [];
    return;
  }
  
  console.log(currentGroup.value)
  console.log('🌸 主香调:', mainFragrance, '次香调:', secondaryFragrance);
  
  try {
    // 检查是否已经从后端获取了图片数据
    let mainImages = [];
    let secondaryImages = [];
    
    // 如果currentGroup.value中已有main_images和secondary_images，直接使用
    if (currentGroup.value.main_images && Array.isArray(currentGroup.value.main_images)) {
      mainImages = currentGroup.value.main_images;
      console.log('✅ 使用后端提供的主香调图片数据:', mainImages);
    }
    
    if (currentGroup.value.secondary_images && Array.isArray(currentGroup.value.secondary_images)) {
      secondaryImages = currentGroup.value.secondary_images;
      console.log('✅ 使用后端提供的次香调图片数据:', secondaryImages);
    }
    
    // 只有在没有图片数据时才调用API获取
    if (mainImages.length === 0 || secondaryImages.length === 0) {
      console.warn('⚠️ 后端未提供图片数据，尝试从API获取');
      if (mainImages.length === 0) {
        const mainResponse = await getFragranceImages(mainFragrance, urlSessionId);
        mainImages = mainResponse.images || [];
      }
      if (secondaryImages.length === 0) {
        const secondaryResponse = await getFragranceImages(secondaryFragrance, urlSessionId);
        secondaryImages = secondaryResponse.images || [];
      }
    }
    
    // 合并所有图片
    const allImages = [...mainImages, ...secondaryImages];
    
    // 如果图片不足8张，使用默认图片填充
    if (allImages.length < 8) {
      console.warn('香调图片不足8张，使用默认图片填充');
      const defaultImages = Array.from({length: 8 - allImages.length}, (_, i) => ({
        label: `默认图片${i + 1}`,
        value: `/images/smell/default/${i + 1}.jpg`,
        image: `/images/smell/default/${i + 1}.jpg`
      }));
      allImages.push(...defaultImages);
    }
    
    // 打乱图片顺序
    const shuffledImages = shuffleArray([...allImages]);
    
    // 只取前8张图片
    const selectedImages = shuffledImages.slice(0, 8);
    
    // 更新题目选项
    question.options = selectedImages;
    
    console.log('🖼️ 已生成香调图片选项:', selectedImages);
  } catch (error) {
    console.error('获取香调图片失败:', error);
    // 使用默认图片作为备选
    const defaultImages = Array.from({length: 8}, (_, i) => ({
      label: `默认图片${i + 1}`,
      value: `/images/smell/default/${i + 1}.jpg`,
      image: `/images/smell/default/${i + 1}.jpg`
    }));
    question.options = defaultImages;
  }
};

// 刷新香调图片选项
const refreshFragranceImages = async () => {
  if (!currentQuestion.value || currentQuestion.value.id !== 'q4') return;
  
  console.log('🔄 刷新香调图片选项...');
  await shuffleFragranceImages(currentQuestion.value);
};

// 获取指定类别的随机图片
const getRandomImagesForCategory = (category, count) => {
  // 确保使用当前URL中的sessionId
  const currentUrl = new URL(window.location.href);
  const urlSessionId = currentUrl.searchParams.get('sessionId');
  
  const images = [];
  const basePath = `/images/smell/${category}/`;
  
  // 假设每个香调类别文件夹中有足够多的图片（1-20.jpg）
  // 随机选择count张不重复的图片
  const availableImages = Array.from({length: 20}, (_, i) => i + 1); // 生成1-20的数字
  const shuffled = shuffleArray([...availableImages]); // 打乱顺序
  
  // 取前count张图片
  for (let i = 0; i < count && i < shuffled.length; i++) {
    const imageNum = shuffled[i];
    const fileName = `${imageNum}.jpg`;
    images.push({
      label: fileName.replace('.jpg', ''), // 使用图片文件名作为选项文字
      value: `${basePath}${fileName}`,
      image: `${basePath}${fileName}`
    });
  }
  
  return images;
};

// 监听当前问题变化
watch(currentQuestion, async (newVal) => {
  if (newVal && newVal.type === 'image-single' && newVal.options && newVal.options.length === 0) {
    // 确保使用当前URL中的sessionId
    const currentUrl = new URL(window.location.href);
    const urlSessionId = currentUrl.searchParams.get('sessionId');
    
    shuffleImages(newVal); // 当切换到新问题时自动加载一组图片
  }
  
  // 处理第四部分图片多选题
  if (newVal && newVal.id === 'q4' && newVal.type === 'image-multiple') {
    console.log('🔄 检测到第四部分图片多选题，准备加载香调图片...');
    // 清空现有选项，确保重新生成
    newVal.options = [];
    await shuffleFragranceImages(newVal); // 当切换到第四部分时自动加载香调图片
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