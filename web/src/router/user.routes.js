const userRoutes = [
    {
        path: '/profile',
        name: 'UserProfile',
        component: () => import('../views/user/UserProfile.vue'),
        meta: { requiresAuth: true, title: '用户信息' },
    },
    {
        path: '/profile/edit',
        name: 'EditProfile',
        component: () => import('../views/user/EditProfile.vue'),
        meta: { requiresAuth: true, title: '编辑个人信息' },
    },
    {
        path: '/users',
        name: 'UserList',
        component: () => import('../views/user/UserList.vue'),
        meta: { requiresAuth: true, title: '用户管理' },
    },
    {
        path: '/users/create',
        name: 'UserCreate',
        component: () => import('../views/user/UserCreate.vue'),
        meta: { requiresAuth: true, title: '创建用户' },
    },
    {
        path: '/users/:id',
        name: 'UserDetail',
        component: () => import('../views/user/UserDetail.vue'),
        meta: { requiresAuth: true, title: '用户详情' },
    },
    {
        path: '/users/:id/edit',
        name: 'AdminUserEdit',
        component: () => import('../views/user/AdminUserEdit.vue'),
        meta: { requiresAuth: true, title: '编辑用户' },
    },
]

export default userRoutes
