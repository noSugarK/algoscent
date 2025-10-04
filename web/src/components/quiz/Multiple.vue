<!-- src/components/quiz/Multiple.vue -->
<template>
  <div class="space-y-4">
    <label
        v-for="option in (question.shuffledOptions || question.options)"
        :key="option.value"
        class="block p-5 border-2 rounded-2xl cursor-pointer transition-all duration-200 transform hover:-translate-y-1 hover:shadow-md"
        :class="multiAnswer.includes(option.value)
        ? 'border-indigo-500 bg-indigo-50'
        : 'border-gray-200 hover:border-gray-300'"
        @click="toggleOption(option.value)"
    >
      <div class="flex items-center">
        <span v-if="option.emoji" class="text-2xl mr-4">{{ option.emoji }}</span>
        <span class="text-gray-800 font-medium">{{ option.label }}</span>
        <span v-if="false && multiAnswer.includes(option.value)" class="ml-auto text-indigo-500">✅</span>
      </div>
    </label>
  </div>
</template>

<script setup>
import { nextTick } from 'vue'
const props = defineProps(['question'])
const multiAnswer = defineModel('multiAnswer')

const toggleOption = (value) => {
  // 添加调试日志
  // console.log('🔍 当前问题ID:', props.question.id);
  // console.log('🔍 当前问题类型:', props.question.type);
  // console.log('🔍 配置的maxSelection:', props.question.maxSelection);
  // console.log('🔍 配置的max_selection:', props.question.max_selection);

  // 优先使用数据库中的max_selection字段，兼容maxSelection
  const max = props.question.max_selection || props.question.maxSelection
  
  // 尝试使用不同的方式更新数组
  const currentAnswers = [...multiAnswer.value];
  // console.log('🔍 选择前的答案数组:', currentAnswers);
  
  let updatedAnswers = [];
  
  if (currentAnswers.includes(value)) {
    // 取消选择
    updatedAnswers = currentAnswers.filter(v => v !== value);
    // console.log('🔍 取消选择后答案数组:', updatedAnswers);
  } else {
    // 选择（未超限）
    if (currentAnswers.length < max) {
      updatedAnswers = [...currentAnswers, value];
      // console.log('🔍 添加选择后答案数组:', updatedAnswers);
    } else {
      // console.log('⚠️ 已达到最大选择数量:', max);
      return; // 未达到最大选择数量时才更新
    }
  }
  
  // 使用nextTick确保异步更新
  nextTick(() => {
    multiAnswer.value = [...updatedAnswers];
    // console.log('✅ multiAnswer已更新:', [...multiAnswer.value]);
  });

  // ✅ 关键：通知父组件答案已更新 → 触发 isAnswered 重新计算
  emit('update');
}

const emit = defineEmits(['update'])
</script>