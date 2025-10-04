import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '../stores/account.js'

// 导入各模块路由
import accountRoutes from './account.routes.js'
import mainRoutes from './main.routes.js'
import userRoutes from './user.routes.js'
import quizRoutes from './quiz.routes.js'

// 合并所有路由
const routes = [
  ...accountRoutes,
  ...mainRoutes,
  ...userRoutes,
  ...quizRoutes,
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

  // 检查是否需要访客状态
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
    return
  }
  
  // 控制测验问题页面的访问
  if (to.path === '/quiz/question') {
    // 允许的来源：测验主页或历史记录页面，或者带有sessionId参数
    const allowedFromPaths = ['/quiz', '/quiz/history']
    const hasSessionId = to.query.sessionId !== undefined
    
    if (!allowedFromPaths.includes(from.path) && !hasSessionId) {
      // 不允许直接访问，重定向到测验主页
      next('/quiz')
      return
    }
  }
  
  // 其他情况允许访问
  next()
})

// 全局后置钩子，用于设置页面标题
router.afterEach((to, from) => {
  // 设置页面标题
  const appName = 'algoscent'
  const title = to.meta.title || '默认页面'
  document.title = `${appName} - ${title}`
})

export default router