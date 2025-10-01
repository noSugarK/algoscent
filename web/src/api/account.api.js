import api from './api'

class AccountService {
  // 用户登录
  async login(username, password, remember_me = false) {
    const response = await api.post('/account/login/', {
      username,
      password,
      remember_me
    })
    return response.data
  }

  // 获取公钥
  async getPublicKey() {
    const response = await api.get('/account/public-key/')
    return response.data
  }

  // 检查用户名是否存在
  async checkUsername(username) {
    const response = await api.post('/account/password/reset/check-username/', {
      username
    })
    return response.data
  }

  // 检查邮箱是否与用户名匹配
  async checkEmail(username, email) {
    const response = await api.post('/account/password/reset/check-email/', {
      username,
      email
    })
    return response.data
  }

  // 忘记密码 - 发送重置邮件
  async forgotPassword(email) {
    const response = await api.post('/account/password/reset/', {
      email
    })
    return response.data
  }

  // 验证密码重置链接
  async validatePasswordResetToken(uid, token) {
    const response = await api.post('/account/password/reset/validate/', {
      uid,
      token
    })
    return response.data
  }

  // 重置密码
  async resetPassword(uid, token, newPassword) {
    const response = await api.post('/account/password/reset/confirm/', {
      uid,
      token,
      new_password: newPassword
    })
    return response.data
  }

  // 刷新token
  async refreshToken(refreshToken) {
    const response = await api.post('/account/token/refresh/', {
      refresh: refreshToken
    })
    return response.data
  }

  // 用户登出
  async logout(refreshToken) {
    try {
      const response = await api.post('/account/logout/', {
        refresh: refreshToken
      })
      return response.data
    } catch (error) {
      console.error('登出请求失败:', error)
      // 即使服务器登出失败，我们也应该清除本地token
      return {}
    }
  }
}

export default new AccountService()