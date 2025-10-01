<template>
  <div class="bg-white rounded-xl overflow-hidden shadow-sm group hover:translate-y-[-6px] transition-transform duration-300">
    <!-- 图片与标签区域 -->
    <div class="relative overflow-hidden">
      <img
          :src="perfume.image"
          :alt="perfume.name"
          class="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div
          class="absolute top-4 right-4 bg-accent/90 text-white text-sm font-medium px-3 py-1 rounded-full"
      >
        {{ perfume.mood }}
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="p-6">
      <h3 class="text-xl font-semibold mb-2">{{ perfume.name }}</h3>
      <p class="text-dark/70 mb-4">{{ perfume.description }}</p>

      <!-- 香调标签 -->
      <div class="flex flex-wrap gap-2 mb-6">
        <span
            v-for="note in perfume.notes"
            :key="note"
            class="text-xs bg-secondary/30 text-dark/70 px-3 py-1 rounded-full"
        >
          {{ note }}
        </span>
      </div>

      <!-- 价格 + 按钮 -->
      <div class="flex justify-between items-center">
        <span class="font-semibold text-lg">{{ perfume.price }}</span>
        <button
            class="bg-primary/10 hover:bg-primary/20 text-primary px-4 py-2 rounded-full transition-colors duration-300"
        >
          了解详情
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 接收香氛对象
defineProps({
  perfume: {
    type: Object,
    required: true
  }
})
</script>