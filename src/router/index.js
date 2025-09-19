import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import QuizHome from "@/views/Quiz/QuizHome.vue";
import AboutView from "@/views/AboutView.vue";
import ProductView from "@/views/ProductView.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/quiz',
    name: 'quiz',
    component: QuizHome
  },
  {
    path: '/product',
    name: 'product',
    component: ProductView
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // 简化滚动行为，移除未使用的参数
    return { top: 0 };
  }
});

export default router;
    