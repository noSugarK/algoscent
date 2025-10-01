import { defineStore } from 'pinia'
import api from '@/api/api.js'

export const useAccountStore = defineStore('auth', {
    state: () => ({
        access_token: null,
        refresh_token: null,
        user: null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.access_token,
    },

    actions: {
        setTokens(access, refresh) {
            this.access_token = access
            this.refresh_token = refresh
            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)
        },

        setUser(user) {
            this.user = user
        },

        clear() {
            this.access_token = null
            this.refresh_token = null
            this.user = null
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
        },

        initializeAuthState() {
            const access = localStorage.getItem('access_token');
            const refresh = localStorage.getItem('refresh_token');

            if (access) {
                this.access_token = access;
            }
            if (refresh) {
                this.refresh_token = refresh;
            }
            // 注意：user 信息通常由 access_token 解析或通过 API 获取，
            // 这里只恢复 token。如果需要恢复 user，可以在此处调用 API。
            // 例如：
            // if (this.access_token) {
            //    // 调用获取用户信息的 API 并 this.setUser(userInfo)
            // }
        },
        
        logout() {
            this.clear();
        },

        // 从API获取用户信息
        async fetchUser() {
            if (!this.access_token) {
                return;
            }

            try {
                const response = await api.get('/users/profile/');
                this.user = response.data;
                return response.data;
            } catch (error) {
                console.error('获取用户信息失败:', error);
                // 如果token无效，清除认证信息
                if (error.response && error.response.status === 401) {
                    this.clear();
                }
                throw error;
            }
        }
    },
})
