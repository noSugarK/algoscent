<template>
  <div 
    id="homeCarousel" 
    class="carousel slide" 
    data-bs-ride="carousel" 
    data-bs-interval="3000" 
    data-bs-pause="hover" 
    data-bs-wrap="true"
    ref="carouselRef"
  >
    <div class="carousel-indicators">
      <button 
        v-for="(slide, index) in slides" 
        :key="index"
        type="button" 
        :data-bs-target="'#homeCarousel'" 
        :data-bs-slide-to="index" 
        :class="{ active: index === 0 }"
        :aria-label="'Slide ' + (index + 1)"
        :aria-current="index === 0 ? 'true' : 'false'">
      </button>
    </div>
    
    <div class="carousel-inner">
      <div 
        v-for="(slide, index) in slides" 
        :key="index"
        class="carousel-item relative"
        :class="{ active: index === 0 }"
      >
        <img 
          :src="slide.image" 
          class="d-block w-100" 
          :alt="slide.title" 
          style="height: auto; max-height: 30rem; object-fit: cover;"
        >
        <!-- 半透明遮罩层，悬停时显示 -->
        <div class="carousel-overlay"></div>
        
        <div class="container">
          <div 
            class="carousel-caption transition-all duration-500 ease-in-out opacity-0 translate-y-4" 
            :class="slide.captionClass"
          >
            <h1>{{ slide.title }}</h1>
            <p>{{ slide.description }}</p>
            <p>
              <a 
                class="btn btn-lg" 
                :class="slide.buttonClass" 
                :href="slide.buttonLink">
                {{ slide.buttonText }}
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <button class="carousel-control-prev" type="button" data-bs-target="#homeCarousel" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#homeCarousel" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Carousel } from 'bootstrap';

const carouselRef = ref(null);
const slides = [
  {
    title: "数据可视化平台",
    description: "为您提供强大的数据分析和可视化功能，帮助您更好地理解和展示数据。",
    buttonText: "立即开始",
    buttonClass: "btn-primary",
    buttonLink: "#",
    captionClass: "text-start",
    image: "/images/logo.png"
  },
  {
    title: "丰富的图表类型",
    description: "支持多种图表类型，包括柱状图、折线图、饼图等，满足各种数据展示需求。",
    buttonText: "了解更多",
    buttonClass: "btn-primary",
    buttonLink: "#",
    captionClass: "text-center",
    image: "/images/logo.png"
  },
  {
    title: "实时数据监控",
    description: "实时监控关键业务指标，及时发现数据异常，为决策提供有力支持。",
    buttonText: "浏览功能",
    buttonClass: "btn-primary",
    buttonLink: "#",
    captionClass: "text-end",
    image: "/images/logo.png"
  }
];

onMounted(() => {
  // 初始化轮播并确保自动播放
  const carousel = new Carousel(carouselRef.value, {
    interval: 3000,
    ride: 'carousel',
    pause: 'hover',
    wrap: true
  });
  
  // 确保轮播自动开始
  carousel.cycle();
  
  // 添加鼠标悬停事件处理
  const carouselItems = document.querySelectorAll('.carousel-item');
  carouselItems.forEach(item => {
    // 鼠标进入时显示标题和按钮
    item.addEventListener('mouseenter', () => {
      const caption = item.querySelector('.carousel-caption');
      const overlay = item.querySelector('.carousel-overlay');
      if (caption) {
        caption.classList.remove('opacity-0', 'translate-y-4');
        caption.classList.add('opacity-100', 'translate-y-0');
      }
      if (overlay) {
        overlay.classList.add('active');
      }
    });
    
    // 鼠标离开时隐藏标题和按钮
    item.addEventListener('mouseleave', () => {
      const caption = item.querySelector('.carousel-caption');
      const overlay = item.querySelector('.carousel-overlay');
      if (caption) {
        caption.classList.remove('opacity-100', 'translate-y-0');
        caption.classList.add('opacity-0', 'translate-y-4');
      }
      if (overlay) {
        overlay.classList.remove('active');
      }
    });
  });
});
</script>

<style scoped>
.carousel {
  margin: 0 auto; /* 居中 */
}

.carousel-item {
  transition: transform 0.6s ease-in-out;
  overflow: hidden;
}

/* 半透明遮罩层样式 */
.carousel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
  pointer-events: none; /* 确保点击能穿透遮罩 */
}

.carousel-overlay.active {
  opacity: 1;
}

.carousel-caption {
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
  bottom: 2rem;
  z-index: 10;
}

.carousel-caption h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.carousel-caption p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  border-radius: 0.5rem;
  transition: transform 0.3s ease;
}

.btn-lg:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .carousel-caption h1 {
    font-size: 1.8rem;
  }
  
  .carousel-caption p {
    font-size: 1rem;
  }
  
  .carousel-inner img {
    height: 20rem !important;
  }
}
</style>
