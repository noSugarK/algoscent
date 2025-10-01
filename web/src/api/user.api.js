import api from './api'

class UserApi {
  // 获取当前用户信息
  async getProfile() {
    try {
      const response = await api.get('/users/profile/')
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '获取用户信息失败')
    }
  }

  // 更新当前用户信息
  async updateProfile(userData) {
    try {
      const response = await api.put('/users/profile/', userData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '更新用户信息失败')
    }
  }

  // 获取指定用户详情
  async getUserDetail(userId) {
    try {
      const response = await api.get(`/users/${userId}/`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '获取用户详情失败')
    }
  }

  // 获取用户列表
  async getUsers(params = {}) {
    try {
      const response = await api.get('/users/', { params })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '获取用户列表失败')
    }
  }

  // 创建用户
  async createUser(userData) {
    try {
      const response = await api.post('/users/', userData)
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data
      if (typeof errorMessage === 'object') {
        const firstErrorKey = Object.keys(errorMessage)[0]
        throw new Error(errorMessage[firstErrorKey][0] || '创建用户失败')
      }
      throw new Error(errorMessage || '创建用户失败')
    }
  }

  // 更新用户
  async updateUser(userId, userData) {
    try {
      const response = await api.put(`/users/${userId}/`, userData)
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data
      if (typeof errorMessage === 'object') {
        const firstErrorKey = Object.keys(errorMessage)[0]
        throw new Error(errorMessage[firstErrorKey][0] || '更新用户失败')
      }
      throw new Error(errorMessage || '更新用户失败')
    }
  }

  // 删除用户
  async deleteUser(userId) {
    try {
      const response = await api.delete(`/users/${userId}/`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '删除用户失败')
    }
  }

  // 检查用户名是否已存在
  async checkUsernameExists(username) {
    try {
      const response = await api.get('/users/check-username/', { params: { username } })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '检查用户名失败')
    }
  }

  // 检查邮箱是否已存在
  async checkEmailExists(email) {
    try {
      const response = await api.get('/users/check-email/', { params: { email } })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || '检查邮箱失败')
    }
  }
}

export default new UserApi()