import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './index.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@fortawesome/fontawesome-free/css/all.min.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'animate.css/animate.min.css';

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)

import { useAccountStore } from './stores/account.js';
const accountStore = useAccountStore();
accountStore.initializeAuthState();

// 如果用户已登录，跳转到主页
if (accountStore.isAuthenticated) {
  accountStore.fetchUser().catch((error) => {
    console.error('获取用户信息失败:', error);
  });
  router.push('/')
}

app.use(router)
app.mount('#app')