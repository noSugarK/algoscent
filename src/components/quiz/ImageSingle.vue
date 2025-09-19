<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <button
        v-for="option in question.options"
        :key="option.value"
        @click="onSelect(option.value)"
        class="rounded-xl overflow-hidden border-2 transition-all duration-200 transform hover:scale-105"
        :class="answer === option.value ? 'border-indigo-500 shadow-lg' : 'border-gray-200'"
    >
      <img :src="option.image" :alt="option.label" class="w-full h-40 md:h-56 object-cover"/>
      <div class="p-2 bg-white">
        <p class="text-sm font-medium text-gray-800">{{ option.label }}</p>
      </div>
    </button>
  </div>
</template>

<script setup>
defineProps(['question'])
const answer = defineModel('answer')

const onSelect = (value) => {
  answer.value = value
  emit('update')
}

const emit = defineEmits(['update'])
</script>