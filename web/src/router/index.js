import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '../stores/account.js'

// 导入各模块路由
import accountRoutes from './account.routes.js'
import mainRoutes from './main.routes.js'
import userRoutes from './user.routes.js'

// 合并所有路由
const routes = [
  ...accountRoutes,
  ...mainRoutes,
  ...userRoutes,
  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '页面未找到' },
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAccountStore()

  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

// 全局后置钩子，用于设置页面标题
router.afterEach((to, from) => {
  // 设置页面标题
  const appName = 'algoscent'
  const title = to.meta.title || '默认页面'
  document.title = `${appName} - ${title}`
})

export default router