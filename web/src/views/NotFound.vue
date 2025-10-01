<template>
  <AppHeader />
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="display-1">404</h1>
      <h2>Not Found</h2>
      <p class="lead">抱歉，您访问的页面不存在。</p>
      <div class="mt-4">
        <router-link to="/" class="btn btn-primary me-2">返回首页</router-link>
        <button class="btn btn-secondary" @click="$router.go(-1)">返回上一页</button>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>

<style scoped>
.not-found-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 600px;
}

.display-1 {
  font-size: 6rem;
  font-weight: 300;
  line-height: 1.2;
  color: #6c757d;
}
</style>