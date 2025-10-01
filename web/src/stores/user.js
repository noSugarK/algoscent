import { defineStore } from 'pinia'
import api from '@/api/api'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        loading: false,
        error: null
    }),

    getters: {
        currentUser: (state) => state.user
    },

    actions: {
        // 获取当前用户信息
        async fetchUserProfile() {
            this.loading = true
            try {
                const response = await api.get('/users/api/v1/profile/')
                this.user = response.data
                return { success: true, data: response.data }
            } catch (error) {
                this.error = error.message
                return { success: false, message: error.message }
            } finally {
                this.loading = false
            }
        },

        // 更新当前用户信息
        async updateUserProfile(userData) {
            this.loading = true
            try {
                const response = await api.put('/users/api/v1/profile/', userData)
                this.user = response.data
                return { success: true, data: response.data }
            } catch (error) {
                this.error = error.message
                return { success: false, message: error.message }
            } finally {
                this.loading = false
            }
        },

        // 获取指定用户详情（管理员功能）
        async fetchUserDetail(userId) {
            this.loading = true
            try {
                const response = await api.get(`/users/api/v1/${userId}/`)
                this.user = response.data
                return { success: true, data: response.data }
            } catch (error) {
                this.error = error.message
                return { success: false, message: error.message }
            } finally {
                this.loading = false
            }
        }
    }
})