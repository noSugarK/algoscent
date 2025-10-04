// 主要页面路由
const quizRoutes = [
    {
        path: '/quiz',
        name: 'Quiz',
        component: () => import('../views/quiz/QuizHome.vue'),
        meta: { requiresAuth: true, title: '测试' },
    },
    // 可以在这里添加更多主要页面路由
]

export default quizRoutes