<template>
  <div class="home">
    <AppHeader />
    <HeroSection />
    <AboutSection />
    <PerfumeSection />
    <TestimonialsSection />
    <CtaSection />
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '../components/layout/AppHeader.vue';
import AppFooter from '../components/layout/AppFooter.vue';
import HeroSection from '../components/home/HeroSection.vue';
import PerfumeSection from '../components/home/PerfumeSection.vue';
import TestimonialsSection from '../components/home/TestimonialsSection.vue';
import CtaSection from '../components/home/CtaSection.vue';
import AboutSection from "@/components/home/AboutSection.vue";
</script>
    