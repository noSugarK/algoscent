<template>
  <section id="about" class="py-20 bg-white">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题区域 -->
      <div class="text-center mb-16">
        <h2 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold mb-4">香氛如何疗愈心灵</h2>
        <p class="text-dark/70 max-w-2xl mx-auto text-lg">
          气味与情绪有着密切的联系，特定的香气能够触发大脑释放让人感觉愉悦的化学物质。
        </p>
      </div>

      <!-- 三栏功能卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- 卡片 1 -->
        <div class="bg-neutral p-8 rounded-xl shadow-sm hover:translate-y-[-6px] transition-transform duration-300">
          <div class="w-14 h-14 bg-primary/20 rounded-full flex items-center justify-center mb-6">
            <i class="fa fa-brain text-primary text-2xl"></i>
          </div>
          <h3 class="text-xl font-semibold mb-3">科学依据</h3>
          <p class="text-dark/70">
            研究表明，某些香气能刺激大脑的边缘系统，促进血清素和多巴胺的释放，有效缓解抑郁和焦虑情绪。
          </p>
        </div>

        <!-- 卡片 2 -->
        <div class="bg-neutral p-8 rounded-xl shadow-sm hover:translate-y-[-6px] transition-transform duration-300">
          <div class="w-14 h-14 bg-primary/20 rounded-full flex items-center justify-center mb-6">
            <i class="fa fa-leaf text-primary text-2xl"></i>
          </div>
          <h3 class="text-xl font-semibold mb-3">天然成分</h3>
          <p class="text-dark/70">
            我们精选全球优质天然精油，不添加有害化学成分，每一款香水都传递着大自然的疗愈力量。
          </p>
        </div>

        <!-- 卡片 3 -->
        <div class="bg-neutral p-8 rounded-xl shadow-sm hover:translate-y-[-6px] transition-transform duration-300">
          <div class="w-14 h-14 bg-primary/20 rounded-full flex items-center justify-center mb-6">
            <i class="fa fa-heart text-primary text-2xl"></i>
          </div>
          <h3 class="text-xl font-semibold mb-3">情绪调节</h3>
          <p class="text-dark/70">
            不同香调针对不同情绪状态，从舒缓压力到提升活力，帮助你找到内心的平衡与和谐。
          </p>
        </div>
      </div>

      <!-- 芳香疗法详情区 -->
      <div class="mt-16 bg-secondary/20 rounded-2xl p-8 md:p-12">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <div class="w-full md:w-1/3">
            <img
              src="https://picsum.photos/id/106/600/800"
              alt="芳香疗法"
              class="rounded-xl shadow-lg w-full h-auto object-cover"
            />
          </div>
          <div class="w-full md:w-2/3 space-y-4">
            <h3 class="text-2xl font-bold">芳香疗法的力量</h3>
            <p class="text-dark/80">
              芳香疗法作为一种自然疗法，已经被使用了数千年。现代科学研究证实，它对缓解抑郁症状、减轻压力和改善睡眠质量有显著效果。
            </p>
            <p class="text-dark/80">
              我们的香水不仅是一种气味，更是一种情绪调节工具。通过每天使用，你可以创造一个持续的自我关怀仪式，逐步改善情绪状态。
            </p>
            <router-link
              to="/quiz"
              class="inline-flex items-center text-primary font-medium hover:underline focus:underline transition"
            >
              发现适合你的疗愈香氛
              <i class="fa fa-arrow-right ml-2"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// 关于我们区域组件
// 确保项目中已引入 Font Awesome 图标库
</script>