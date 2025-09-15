<template>
  <header class="bg-white shadow-sm">
    <div class="container mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold text-primary">疗愈香氛</router-link>
        
        <nav class="hidden md:flex space-x-8">
          <router-link to="/" class="hover:text-primary transition-colors">首页</router-link>
          <router-link to="/quiz" class="hover:text-primary transition-colors">香氛测试</router-link>
          <a href="#" class="hover:text-primary transition-colors">产品系列</a>
          <a href="#" class="hover:text-primary transition-colors">关于我们</a>
        </nav>
        
        <button class="md:hidden">
          <i class="fa fa-bars text-xl"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
// 头部导航组件
</script>

<style scoped>
.text-primary {
  color: #7b61ff;
}
</style>
    