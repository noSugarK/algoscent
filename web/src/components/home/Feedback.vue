<template>
  <section id="testimonials" class="py-20 bg-gradient-to-b from-neutral to-secondary">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题区 -->
      <div class="text-center mb-16">
        <h2 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold mb-4">用户的疗愈之旅</h2>
        <p class="text-dark/70 max-w-2xl mx-auto text-lg">
          听听那些通过我们的香氛找到了内心平静的人们怎么说
        </p>
      </div>

      <!-- 评价卡片网格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <TestimonialCard
            v-for="testimonial in testimonials"
            :key="testimonial.id"
            :image-src="testimonial.imageSrc"
            :name="testimonial.name"
            :text="testimonial.text"
            :product="testimonial.product"
            :rating="testimonial.rating"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import TestimonialCard from '@/components/ui/FeedbackCard.vue'

// 用户评价数据（保留原始情感文案）
const testimonials = [
  {
    id: 1,
    imageSrc: 'https://picsum.photos/id/64/100/100',
    name: '林小姐',
    text: '患抑郁症两年多，尝试了很多方法。自从使用"森林低语"后，每天晚上都能感受到一种平静。它的木质香调让我感到安全，仿佛被拥抱一般。',
    product: '森林低语',
    rating: 5 // 5 星
  },
  {
    id: 2,
    imageSrc: 'https://picsum.photos/id/91/100/100',
    name: '张先生',
    text: '工作压力大，经常失眠焦虑。"薰衣草梦境"成了我的救星，每晚睡前使用，能明显感觉到神经放松下来，入睡也变得容易多了。推荐给所有压力大的朋友。',
    product: '薰衣草梦境',
    rating: 4.5 // 4.5 星（支持半星）
  },
  {
    id: 3,
    imageSrc: 'https://picsum.photos/id/26/100/100',
    name: '王女士',
    text: '季节性抑郁让我每年冬天都很痛苦。"阳光柑橘"的清新香气仿佛把阳光带入了我的生活，即使在阴霾的日子里，也能感受到一丝温暖和希望。',
    product: '阳光柑橘',
    rating: 5 // 5 星
  }
]
</script>