import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/questionnaire',
    name: 'questionnaire',
    component: HomeView
  }
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
    