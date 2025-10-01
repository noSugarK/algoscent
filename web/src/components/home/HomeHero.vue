<template>
  <section
      id="home"
      class="pt-28 pb-20 md:pt-40 md:pb-32 bg-gradient-to-b from-secondary/30 to-neutral"
  >
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col lg:flex-row items-center">
        <!-- 文案区域 -->
        <div class="w-full lg:w-1/2 mb-10 lg:mb-0">
          <h1 class="text-[clamp(2.5rem,5vw,4rem)] font-bold leading-tight text-dark mb-6">
            找到专属于你的<br />
            <span class="text-primary">疗愈香氛</span>
          </h1>
          <p class="text-lg md:text-xl text-dark/80 mb-8 max-w-lg">
            每个人的心灵都值得被温柔呵护。通过我们的香氛测试，发现最能安抚你情绪的自然香气。
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <router-link
                to="/quiz"
                class="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-full font-medium transition-smooth text-center"
            >
              开始测试
            </router-link>
            <a
                href="#perfumes"
                class="border-2 border-primary text-primary hover:bg-primary/10 px-8 py-3 rounded-full font-medium transition-smooth text-center"
            >
              探索香氛系列
            </a>
          </div>
        </div>

        <!-- 轮播图区域 -->
        <div class="w-full lg:w-1/2 relative">
          <!-- 轮播容器 -->
          <div class="relative z-10 rounded-2xl overflow-hidden shadow-2xl min-h-[400px] group">
            <!-- 图片项 -->
            <div
                v-for="(item, index) in images"
                :key="index"
                class="absolute inset-0 transition-opacity duration-700 ease-in-out"
                :class="{
                'opacity-100 z-10': current === index,
                'opacity-0': current !== index
              }"
            >
              <img
                  :src="item.src"
                  :alt="item.alt"
                  class="w-full h-full object-cover"
              />
            </div>

            <!-- 左右箭头（仅 hover 显示） -->
            <button
                @click="prev"
                class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full z-20 transition-opacity duration-300 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto"
                aria-label="上一张"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
                @click="next"
                class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full z-20 transition-opacity duration-300 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto"
                aria-label="下一张"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- 指示器（保持常显） -->
            <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2 z-20">
              <button
                  v-for="(item, index) in images"
                  :key="index"
                  @click="current = index"
                  class="w-3 h-3 rounded-full transition"
                  :class="{
                  'bg-white': current === index,
                  'bg-white/50': current !== index
                }"
                  :aria-label="`跳转到第${index + 1}张`"
              ></button>
            </div>
          </div>

          <!-- 背景光晕 -->
          <div class="absolute top-10 -right-5 w-64 h-64 bg-accent/20 rounded-full blur-3xl -z-10"></div>
          <div class="absolute -bottom-10 -left-5 w-72 h-72 bg-primary/20 rounded-full blur-3xl -z-10"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const images = ref([
  {
    src: '/images/logo.png',
    alt: '疗愈香氛产品展示 1'
  },
  {
    src: '/images/paperwall_2.jpg',
    alt: '疗愈香氛产品展示 2'
  },
  {
    src: '/images/paperwall_2.jpg',
    alt: '疗愈香氛产品展示 3'
  }
])

const current = ref(0)
let interval = null

const next = () => {
  current.value = (current.value + 1) % images.value.length
}

const prev = () => {
  current.value = (current.value - 1 + images.value.length) % images.value.length
}

onMounted(() => {
  interval = setInterval(next, 4000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
/* 可选：优化淡入动画 */
.opacity-100 {
  opacity: 1;
  animation: fadeIn 0.7s ease-in-out;
  will-change: opacity;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>