import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// 关键：导入本地 Tailwind CSS 文件（路径必须完全正确）
import './assets/css/tailwind.css';
// 关键：导入本地 Font Awesome
import '@fortawesome/fontawesome-free/css/all.min.css';

const app = createApp(App);
app.use(router);
app.mount('#app');
