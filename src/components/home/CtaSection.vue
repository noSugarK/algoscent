<template>
  <section class="py-20 bg-gradient-to-b from-primary/5 to-neutral">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题区 -->
      <div class="max-w-3xl mx-auto text-center mb-16">
        <h2 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold mb-4">找到你的疗愈香氛</h2>
        <p class="text-dark/70 text-lg">
          每个人的情绪需求都是独特的，通过我们的个性化测试，发现最适合你的疗愈香氛。
        </p>
      </div>

      <!-- 内容卡片 -->
      <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div class="p-8 md:p-12">
            <div class="flex flex-col md:flex-row items-center gap-8">
              <!-- 文案区 -->
              <div class="w-full md:w-1/2">
                <h3 class="text-2xl font-bold mb-4">个性化香氛推荐</h3>
                <p class="text-dark/80 mb-6">
                  完成我们简单的情绪评估问卷，基于你的状态和需求，获得量身定制的香氛推荐，帮助你走上情绪疗愈之路。
                </p>

                <!-- 特性列表 -->
                <ul class="space-y-3 mb-8">
                  <li class="flex items-start" v-for="feature in features" :key="feature">
                    <i class="fa fa-check-circle text-primary mt-1 mr-3"></i>
                    <span>{{ feature }}</span>
                  </li>
                </ul>

                <!-- 按钮 -->
                <router-link
                  to="/questionnaire"
                  class="inline-block bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-full font-medium transition-colors duration-300"
                >
                  开始测试 <i class="fa fa-arrow-right ml-2"></i>
                </router-link>
              </div>

              <!-- 图片区 -->
              <div class="w-full md:w-1/2">
                <img
                  src="https://picsum.photos/id/366/600/400"
                  alt="香氛测试"
                  class="rounded-xl shadow-md w-full h-auto"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// 定义特性列表，便于维护和国际化
const features = [
  '根据你的情绪状态定制推荐',
  '了解不同香调对你情绪的影响',
  '获取专业的香氛使用建议'
]
</script>

<style scoped>
/* 如果你使用的是 Tailwind，以下 style 可省略 */
/* 但保留以支持自定义主题色 */
.bg-primary {
  background-color: #7b61ff;
}
.text-primary {
  color: #7b61ff;
}
.from-primary\/5 {
  background: linear-gradient(to bottom, rgba(123, 97, 255, 0.05), #f8f9fa);
}
</style>