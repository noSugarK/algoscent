<template>
  <div class="space-y-4">
    <label
        v-for="option in (question.shuffledOptions || question.options)"
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
        <span v-if="option.emoji" class="text-2xl mr-4">{{ option.emoji }}</span>
        <span class="text-gray-800 font-medium">{{ option.label }}</span>
      </div>
    </label>
  </div>
</template>

<script setup>
defineProps(['question'])
const answer = defineModel('answer')
</script>