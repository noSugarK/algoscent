<!-- src/components/quiz/Multiple.vue -->
<template>
  <div class="space-y-4">
    <label
        v-for="option in question.options"
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
const props = defineProps(['question'])
const multiAnswer = defineModel('multiAnswer')

const toggleOption = (value) => {
  const max = props.question.maxSelection || 3

  if (multiAnswer.value.includes(value)) {
    // 取消选择
    multiAnswer.value = multiAnswer.value.filter(v => v !== value)
  } else {
    // 选择（未超限）
    if (multiAnswer.value.length < max) {
      multiAnswer.value.push(value)
    }
  }

  // ✅ 关键：通知父组件答案已更新 → 触发 isAnswered 重新计算
  emit('update')
}

const emit = defineEmits(['update'])
</script>