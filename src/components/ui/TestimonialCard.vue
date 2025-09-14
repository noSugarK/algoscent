<!-- src/components/ui/TestimonialCard.vue -->
<template>
  <div class="bg-neutral p-8 rounded-xl shadow-sm hover:shadow-md transition-all duration-300">
    <div class="flex items-center mb-6">
      <img :src="imageSrc" :alt="name" class="w-14 h-14 rounded-full object-cover mr-4" />
      <div>
        <h4 class="font-semibold">{{ name }}</h4>
        <div class="flex mt-1">
          <!-- 使用组件 -->
          <StarRating :rating="rating" />
        </div>
      </div>
    </div>

    <p class="text-dark/80 italic mb-4">"{{ text }}"</p>
    <p class="text-dark/60 text-sm">使用产品：{{ product }}</p>
  </div>
</template>

<script setup>
import StarRating from './StarRating.vue'

defineProps({
  imageSrc: String,
  name: String,
  text: String,
  product: String,
  rating: {
    type: Number,
    validator: value => value >= 1 && value <= 5
  }
})
</script>