<template>
  <header class="bg-white shadow-sm">
    <div class="container mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <router-link to="/" class="flex items-center space-x-2 text-2xl font-bold text-primary">
          <img src="/logo.png" width="200px" alt="Logo" />
        </router-link>

        <!-- 桌面端导航 -->
        <nav class="hidden md:flex space-x-8">
          <router-link to="/" class="hover:text-primary transition-colors">首页</router-link>
          <router-link to="/quiz" class="hover:text-primary transition-colors">香氛测试</router-link>
          <router-link to="/product" class="hover:text-primary transition-colors">产品系列</router-link>
          <router-link to="/about" class="hover:text-primary transition-colors">关于我们</router-link>
        </nav>

        <!-- 移动端菜单按钮 -->
        <button @click="isMenuOpen = !isMenuOpen" class="md:hidden p-2">
          <i class="fa fa-bars text-xl"></i>
        </button>
      </div>

      <!-- 移动端下拉菜单 -->
      <div v-show="isMenuOpen" class="md:hidden mt-4 pb-4 border-t">
        <nav class="flex flex-col space-y-4">
          <router-link to="/" class="hover:text-primary transition-colors" @click="isMenuOpen = false">首页</router-link>
          <router-link to="/quiz" class="hover:text-primary transition-colors" @click="isMenuOpen = false">香氛测试</router-link>
          <router-link to="/product" class="hover:text-primary transition-colors" @click="isMenuOpen = false">产品系列</router-link>
          <router-link to="/about" class="hover:text-primary transition-colors" @click="isMenuOpen = false">关于我们</router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

// 控制移动端菜单开关
const isMenuOpen = ref(false)
</script>

<style scoped>
.text-primary {
  color: #007BFF;
}
</style>