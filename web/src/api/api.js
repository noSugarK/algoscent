import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api/v1', // 基础URL，根据实际情况调整
  timeout: 10000, // 请求超时时间
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理特定的错误状态码
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
          break
        case 403:
          // 禁止访问
          console.error('访问被拒绝')
          break
        case 500:
          // 服务器错误
          console.error('服务器内部错误')
          break
        default:
          console.error('请求错误', error.response.data)
      }
    }
    return Promise.reject(error)
  }
)

export default api