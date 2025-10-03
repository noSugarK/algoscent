<template>
  <AppHeader />
  <Carousel />
  <HomeHero />
  <Perfume />
  <Feedback />
  <AppFooter />
</template>

<script setup>
import { useAccountStore } from '../stores/account.js'
import { onMounted } from 'vue'
import AppHeader from "@/components/layout/AppHeader.vue"
import AppFooter from "@/components/layout/AppFooter.vue"
import Carousel from "@/components/home/Carousel.vue"
import HomeHero from '@/components/home/HomeHero.vue'
import Perfume from '@/components/home/Perfume.vue'
import Feedback from '@/components/home/Feedback.vue'

const accountStore = useAccountStore()

// 页面加载时获取用户信息
onMounted(async () => {
  if (accountStore.isAuthenticated && !accountStore.user) {
    try {
      await accountStore.fetchUser()
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }
})
</script>

<style scoped>

</style>