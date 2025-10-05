<template>
  <div class="text-question">
    <div class="textarea-container">
      <textarea
        v-model="textAnswer"
        :placeholder="question.placeholder || '请在此输入您的答案...'"
        class="w-full p-4 border border-gray-300 rounded-xl resize-y min-h-[120px] transition-all focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 focus:outline-none"
        @input="handleInput"
      ></textarea>
    </div>
    
    <div class="flex justify-end mt-3">
      <button
        @click="handleAIExtend"
        :disabled="!textAnswer?.trim() || loading"
        class="flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors"
        :class="{
          'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600': textAnswer?.trim() && !loading,
          'bg-gray-200 text-gray-400 cursor-not-allowed': !textAnswer?.trim() || loading
        }"
      >
        <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ loading ? 'AI扩写中...' : 'AI扩写' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {extendTextWithAI} from '@/api/quiz.api.js'

const props = defineProps({
  question: {
    type: Object,
    required: true
  }
})

// 使用defineModel实现双向绑定，与SingleWithText.vue保持一致
const textAnswer = defineModel('textAnswer')
const emit = defineEmits(['update'])
const loading = ref(false)

const handleInput = () => {
  // 使用update事件通知父组件
  emit('update')
}

const handleAIExtend = async () => {
  if (!textAnswer.value?.trim() || loading.value) return
  
  loading.value = true
  try {
    const result = await extendTextWithAI(textAnswer.value)
    if (result && result.extended_text) {
      textAnswer.value = result.extended_text
      emit('update')
    }
  } catch (error) {
    console.error('AI扩写失败:', error)
    alert('AI扩写失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.text-question {
  font-family: inherit;
}

.textarea-container {
  position: relative;
}

textarea {
  font-family: inherit;
  font-size: 16px;
  line-height: 1.6;
}

button {
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
}
</style>