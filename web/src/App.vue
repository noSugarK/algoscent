<template>
  <div id="app" :style="backgroundStyle">
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      backgroundImage: 'url(./images/background.jpg)', // 动态背景图片路径
      backgroundColor: '#abe386' // 动态背景颜色
    }
  },
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: this.backgroundImage,
        backgroundColor: this.backgroundColor,
        backgroundSize: 'cover',
        height: '100%', // 视窗高度，确保背景覆盖整个页面
        width: '100%' // 视窗宽度
      };
    }
  }
}
</script>