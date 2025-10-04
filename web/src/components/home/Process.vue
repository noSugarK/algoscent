<template>
  <div class="py-12">
    <div class="container">
      <h2 class="text-3xl font-bold text-center mb-12">工艺流程</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- 精心培育步骤 -->
        <div class="process-step transition-all duration-300 hover:shadow-lg rounded-lg overflow-hidden bg-white">
          <div class="process-image relative">
            <img 
              src="/images/home/cultivation.jpg" 
              alt="精心培育" 
              class="w-full h-64 object-cover"
              v-on:error="handleImageError($event, '/images/default_process.jpg')"
            >
            <div class="process-number absolute top-4 left-4 w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center text-xl font-bold">1</div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-semibold mb-3">精心培育</h3>
            <p class="text-gray-600">我们精选优质原材料，通过科学的培育方法，确保每一种原料都达到最佳品质。严格控制生长环境，采用有机种植方式，不使用化学农药和肥料。</p>
          </div>
        </div>
        
        <!-- 科学调配步骤 -->
        <div class="process-step transition-all duration-300 hover:shadow-lg rounded-lg overflow-hidden bg-white">
          <div class="process-image relative">
            <img 
              src="/images/home/blending.jpg" 
              alt="科学调配" 
              class="w-full h-64 object-cover"
              v-on:error="handleImageError($event, '/images/default_process.jpg')"
            >
            <div class="process-number absolute top-4 left-4 w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center text-xl font-bold">2</div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-semibold mb-3">科学调配</h3>
            <p class="text-gray-600">由专业调香师团队，根据多年经验和科学配方，精确调配各种原料比例。采用先进的萃取技术，保留原料的天然香气和活性成分。</p>
          </div>
        </div>
        
        <!-- 精致搭配步骤 -->
        <div class="process-step transition-all duration-300 hover:shadow-lg rounded-lg overflow-hidden bg-white">
          <div class="process-image relative">
            <img 
              src="/images/home/matching.jpg" 
              alt="精致搭配" 
              class="w-full h-64 object-cover"
              v-on:error="handleImageError($event, '/images/default_process.jpg')"
            >
            <div class="process-number absolute top-4 left-4 w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center text-xl font-bold">3</div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-semibold mb-3">精致搭配</h3>
            <p class="text-gray-600">将调配好的原料进行精致搭配，通过多层次的香气组合，创造出独特的嗅觉体验。每一款产品都经过反复测试和调整，确保品质稳定。</p>
          </div>
        </div>
        
        <!-- 使用教程步骤 -->
        <div class="process-step transition-all duration-300 hover:shadow-lg rounded-lg overflow-hidden bg-white">
          <div class="process-image relative">
            <img 
              src="/images/home/tutorial.jpg" 
              alt="使用教程" 
              class="w-full h-64 object-cover"
              v-on:error="handleImageError($event, '/images/default_process.jpg')"
            >
            <div class="process-number absolute top-4 left-4 w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center text-xl font-bold">4</div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-semibold mb-3">使用教程</h3>
            <p class="text-gray-600">提供详细的使用指南和技巧，帮助您充分发挥产品功效。包括最佳使用时间、用量控制、存储方法等专业建议，让您获得最佳体验。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

// 处理图片加载错误的函数
const handleImageError = (event, fallbackImage) => {
  event.target.src = fallbackImage;
};
</script>

<style scoped>
/* 工艺步骤容器样式 */
#processDisplay {
  background-color: #f8f9fa;
}

/* 单个步骤样式 */
.process-step {
  border: 1px solid #e9ecef;
}

.process-step:hover {
  transform: translateY(-5px);
}

/* 步骤图片样式 */
.process-image {
  overflow: hidden;
}

.process-image img {
  transition: transform 0.5s ease;
}

.process-step:hover .process-image img {
  transform: scale(1.05);
}

/* 步骤数字样式 */
.process-number {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .process-step {
    margin-bottom: 2rem;
  }
}

@media (max-width: 768px) {
  h2 {
    font-size: 2rem !important;
  }
  
  .process-step h3 {
    font-size: 1.5rem;
  }
  
  .process-image img {
    height: 48px;
  }
}

@media (max-width: 576px) {
  #processDisplay {
    padding: 2rem 1rem;
  }
  
  h2 {
    font-size: 1.8rem !important;
  }
}

/* 主题颜色变量 */
:root {
  --primary-color: #007bff;
}

.bg-primary {
  background-color: var(--primary-color);
}

.text-primary {
  color: var(--primary-color);
}
</style>
