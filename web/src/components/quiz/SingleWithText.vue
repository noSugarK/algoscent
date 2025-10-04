<template>
  <div class="space-y-6">
    <!-- 单选选项 -->
    <label
        v-for="option in question.options"
        :key="option.value"
        class="block p-5 border-2 border-gray-200 rounded-2xl cursor-pointer hover:border-indigo-300 hover:shadow-md transition-all duration-200 transform hover:-translate-y-1"
        :class="answer === option.value ? 'border-indigo-500 bg-indigo-50' : ''"
    >
      <input
          type="radio"
          :value="option.value"
          v-model="answer"
          class="hidden"
      />
      <div class="flex items-center">
        <span class="text-gray-800 font-medium">{{ option.label }}</span>
      </div>
    </label>

    <!-- 条件填空 -->
    <div v-if="answer && showTextWhen && answer === showTextWhen" class="mt-6 pt-4 border-t border-gray-100">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ props.question.textFollowUp || '请补充说明：' }}
      </label>
      <textarea
          v-model="textAnswer"
          :placeholder="props.question.placeholder || '请输入...'"
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          :rows="props.question.rows || 3"
          @input="$emit('update')"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const answer = defineModel('answer')
const textAnswer = defineModel('textAnswer')

// 创建一个响应式的showTextWhen副本，避免直接修改props
const showTextWhen = ref(props.question.showTextWhen || '')

// 监听question变化，更新showTextWhen
watchEffect(() => {
  // 针对第19题(q2-9)的特殊处理
  if (props.question.id === 'q2-9' && !props.question.showTextWhen) {
    showTextWhen.value = 'yes'
  } else {
    showTextWhen.value = props.question.showTextWhen || ''
  }
})

// 使用watchEffect监听answer变化，避免闭包问题
watchEffect(() => {
  if (answer.value && props.question.options) {
    // 检查是否选择了需要显示文本框的选项
    if ((answer.value === 'yes' || 
         props.question.options.some(opt => 
           opt.value === answer.value && 
           opt.label.includes('有使用过')))) {
      // 确保textAnswer有初始值
      if (!textAnswer.value) {
        textAnswer.value = ''
      }
    }
  }
})

// 暴露showTextWhen给模板使用
defineExpose({
  showTextWhen
})
</script>