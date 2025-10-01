<!-- src/components/account/SocialIntroCard.vue -->
<template>
  <div class="social-intro-card d-none d-lg-flex flex-column justify-content-center align-items-center p-5 text-center">
    <router-link to="/about"><h3 class="text-green-100 fw-bold mb-3">关注我们</h3></router-link>
    <p class="text-base mb-4" style="max-width: 300px;">
      获取最新动态、产品更新和独家优惠。加入我们的社区，与数万用户一起探索数据之美。
    </p>

    <!-- 当前选中的二维码 -->
    <div class="mb-4">
      <img
          :src="currentQrCode"
          alt="扫码关注"
          class="qr-code-image"
      />
    </div>

    <!-- 社交图标切换按钮 -->
    <div class="social-links d-flex justify-content-center gap-4">
      <a
          href="#"
          class="text-white fs-5 icon-btn"
          :class="{ active: activeTab === 'weixin' }"
          @click.prevent="setActive('weixin')"
      >
        <i class="fa-brands fa-weixin"></i>
      </a>
      <a
          href="#"
          class="text-white fs-5 icon-btn"
          :class="{ active: activeTab === 'weibo' }"
          @click.prevent="setActive('weibo')"
      >
        <i class="fa-brands fa-weibo"></i>
      </a>
      <a
          href="#"
          class="text-white fs-5 icon-btn"
          :class="{ active: activeTab === 'qq' }"
          @click.prevent="setActive('qq')"
      >
        <i class="fa-brands fa-qq"></i>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 图片路径映射（请确保这些图片存在于 public/images/qrcode/ 路径下）
const qrCodes = {
  weixin: '/images/qrcode/weixin.png',
  weibo: '/images/qrcode/weibo.png',
  qq: '/images/qrcode/qq.png'
}

const activeTab = ref('weixin')

// 动态返回当前二维码图片
const currentQrCode = computed(() => {
  return qrCodes[activeTab.value] || qrCodes.weixin
})

// 设置当前激活的平台
const setActive = (platform) => {
  activeTab.value = platform
}
</script>

<style scoped>
.social-intro-card {
  width: 400px;
  height: 500px;
  backdrop-filter: blur(10px);
  border-radius: 0 15px 15px 0;
  transition: transform 0.3s ease;
}

.social-intro-card:hover {
  transform: scale(1.02);
}

.social-intro-card h3 {
  font-size: 1.8rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.social-intro-card p {
  line-height: 1.6;
}

/* 二维码样式 */
.qr-code-image {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* 社交图标按钮 */
.icon-btn {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.icon-btn:hover,
.icon-btn.active {
  transform: scale(1.2);
  background-color: rgb(59, 145, 10);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.icon-btn.active {
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
}
</style>