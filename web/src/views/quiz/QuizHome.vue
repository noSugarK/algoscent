<template>
  <AppHeader />
  <div class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4 flex items-center justify-center">
    <!-- 首页 -->
    <div v-if="!showQuiz" class="max-w-3xl mx-auto bg-white rounded-3xl shadow-xl p-10 md:p-12 border border-gray-100">
      <div class="text-center mb-10">
        <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-6">
          🌿 疗愈香氛偏好测试
        </h1>
        <p class="text-gray-600 text-lg leading-relaxed">
          花约2分钟，帮助我们了解你的情绪、审美与生活方式，为你定制专属疗愈香氛方案。
        </p>
      </div>

      <div class="bg-gray-50 rounded-2xl p-8 mb-8 text-left space-y-4">
        <h3 class="font-bold text-gray-800 text-lg">📋 问卷说明</h3>
        <ul class="list-disc list-inside space-y-2 text-gray-700">
          <li>共4个部分，约25题，预计耗时10分钟</li>
          <li>所有信息仅用于香氛推荐，严格保密</li>
          <li>请根据第一直觉作答，无对错之分</li>
          <li>部分题目会根据你的选择动态调整</li>
        </ul>
      </div>

      <div class="flex items-center mb-8">
        <input
            id="agree"
            type="checkbox"
            v-model="agreed"
            class="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
        />
        <label for="agree" class="ml-3 text-gray-700">
          我已阅读并同意以上说明，自愿参与测试
        </label>
      </div>

      <button
          @click="startQuiz"
          :disabled="!agreed"
          class="w-full py-4 px-8 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 text-white font-bold rounded-xl text-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed"
      >
        🚀 开始测试
      </button>

      <div class="mt-8 text-center text-sm text-gray-500">
        点击开始即表示你授权我们基于你的答案生成个性化推荐
      </div>
    </div>

    <!-- 问卷组件 -->
    <Question
        v-else
        @complete="onQuizComplete"
        @restart="onQuizRestart"
        ref="quizRef"
        class="w-full"
    />
  </div>
  <AppFooter />
</template>

<script setup>
import { ref } from 'vue'
import Question from './Question.vue'
import AppHeader from "@/components/layout/AppHeader.vue";
import AppFooter from "@/components/layout/AppFooter.vue";

const agreed = ref(false)
const showQuiz = ref(false)
const quizRef = ref(null)

const startQuiz = () => {
  if (agreed.value) {
    showQuiz.value = true
  }
}

const onQuizComplete = (report) => {
  console.log('✅ 问卷完成:', report)
  // 可跳转结果页、或弹窗、或保持在此展示
}

const onQuizRestart = () => {
  if (quizRef.value) {
    quizRef.value.reset() // 调用子组件暴露的方法
  }
  showQuiz.value = false
}
</script>