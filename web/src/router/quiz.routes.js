// 主要页面路由
const quizRoutes = [
    {
        path: '/quiz',
        name: 'Quiz',
        component: () => import('../views/quiz/QuizHome.vue'),
        meta: { requiresAuth: true, title: '测试' },
    },
    {
        path: '/quiz/question',
        name: 'Question',
        component: () => import('../views/quiz/Question.vue'),
        meta: { requiresAuth: true, title: '开始测试' },
    },
    {
        path: '/quiz/history',
        name: 'QuizHistory',
        component: () => import('../views/quiz/History.vue'),
        meta: { requiresAuth: true, title: '历史记录' },
    },
    {
        path: '/quiz/report/:sessionId',
        name: 'QuizReport',
        component: () => import('../views/quiz/ReportDetail.vue'),
        meta: { requiresAuth: true, title: '测验报告' },
    },
]

export default quizRoutes