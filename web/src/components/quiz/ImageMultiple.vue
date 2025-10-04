<template>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    <button
        v-for="option in question.options"
        :key="option.value"
        @click="toggleOption(option.value)"
        class="rounded-xl overflow-hidden border-2 transition-all duration-200 transform hover:scale-105"
        :class="multiAnswer.includes(option.value) ? 'border-indigo-500 shadow-lg bg-indigo-50' : 'border-gray-200'"
    >
      <div class="relative">
        <img :src="option.image" :alt="option.label" class="w-full h-24 md:h-28 object-cover"/>
        <div v-if="multiAnswer.includes(option.value)"
             class="absolute top-2 right-2 w-6 h-6 bg-indigo-500 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
      </div>
      <div class="p-2 bg-white">
        <p class="text-xs font-medium text-gray-800 text-center">{{ option.label }}</p>
      </div>
    </button>
    <div v-if="multiAnswer.length > (question.max_selection || question.maxSelection)"
         class="col-span-full text-center mt-2 text-red-500 text-sm">
      ⚠️ 最多选择 {{ question.max_selection || question.maxSelection }} 项
    </div>
  </div>
</template>

<script setup>
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
  if (multiAnswer.value.includes(value)) {
    // 取消选择 - 创建新数组引用
    multiAnswer.value = [...multiAnswer.value.filter(v => v !== value)]
  } else {
    // 选择（未超限） - 创建新数组引用
    if (multiAnswer.value.length < max) {
      multiAnswer.value = [...multiAnswer.value, value]
    }
  }
  emit('update')
}

const emit = defineEmits(['update'])
</script>