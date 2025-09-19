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
    <div v-if="answer === question.showTextWhen" class="mt-6 pt-4 border-t border-gray-100">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ question.textFollowUp || '请补充说明：' }}
      </label>
      <textarea
          v-model="textAnswer"
          :placeholder="question.placeholder || '请输入...'"
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          :rows="question.rows || 3"
          @input="$emit('update')"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
defineProps(['question'])
const answer = defineModel('answer')
const textAnswer = defineModel('textAnswer')
</script>