// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// 使用 defineStore 创建一个 store，'useAuthStore' 是它的唯一 ID
export const useAuthStore = defineStore('auth', () => {
  // --- State (状态) ---
  // 使用 ref 创建响应式状态，初始值从浏览器的 localStorage 读取
  const token = ref(localStorage.getItem('jwt_token'))
  const router = useRouter()

  // --- Getters (计算属性) ---
  // 创建一个计算属性，方便地判断用户是否已登录
  const isAuthenticated = computed(() => !!token.value)

  // --- Actions (方法) ---

  /**
   * 存储 token 到 Pinia 和 localStorage
   * @param {string} newToken - 从后端获取到的 JWT token
   */
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('jwt_token', newToken)
  }

  /**
   * 清除 token，用于登出
   */
  function clearToken() {
    token.value = null
    localStorage.removeItem('jwt_token')
  }

  /**
   * 登出并跳转到登录页
   */
  function logout() {
    clearToken()
    router.push('/') // 跳转回登录页
  }

  // 必须返回所有需要暴露给外部使用的 state, getters, 和 actions
  return {
    token,
    isAuthenticated,
    setToken,
    clearToken,
    logout,
  }
})
