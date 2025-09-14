// src/services/api.js
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// 1. 创建一个 Axios 实例
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // 后端 API 的基础 URL
  headers: {
    'Content-Type': 'application/json',
  },
})

// 2. 添加一个请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 在每个请求发送前，都来这里检查一下
    const authStore = useAuthStore()
    const token = authStore.token

    if (token) {
      // 如果有 token，就在请求头里加上 'Authorization'
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // 如果请求出错，直接拒绝
    return Promise.reject(error)
  },
)

// 3. 导出这个配置好的实例
export default apiClient
