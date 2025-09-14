<template>
  <section id="perfumes" class="py-20 bg-neutral">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题区 -->
      <div class="text-center mb-16">
        <h2 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold mb-4">疗愈香氛系列</h2>
        <p class="text-dark/70 max-w-2xl mx-auto text-lg">
          每一款都为特定情绪状态精心调配，帮助你找回内心的平静与力量
        </p>
      </div>

      <!-- 香氛卡片网格 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <PerfumeCard
          v-for="perfume in perfumes"
          :key="perfume.id"
          :perfume="perfume"
        />
      </div>

      <!-- 查看全部按钮 -->
      <div class="text-center mt-12">
        <a
          href="#all"
          class="inline-flex items-center bg-white border border-primary text-primary hover:bg-primary/10 px-8 py-3 rounded-full font-medium transition duration-300 ease-smooth"
        >
          查看全部香氛
          <i class="fa fa-long-arrow-right ml-2"></i>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { product } from '@/composables/product'
import PerfumeCard from '@/components/ui/PerfumeCard.vue'

const { perfumes } = product()
</script>