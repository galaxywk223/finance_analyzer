<!-- src/views/LoginView.vue -->
<script setup>
import { ref } from 'vue'
import axios from 'axios'
// 确保这里导入了 RouterLink
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/login', {
      username: username.value,
      password: password.value,
    })
    const token = response.data.token
    authStore.setToken(token)
    router.push({ name: 'dashboard' })
  } catch (error) {
    console.error('登录失败:', error.response)
    if (error.response && error.response.data.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = '发生未知错误，请稍后再试。'
    }
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-yellow-100">
    <div
      class="w-full max-w-sm p-8 space-y-6 bg-white rounded-3xl shadow-lg transform hover:scale-105 transition-transform duration-300"
    >
      <div class="text-center">
        <h1 class="text-4xl font-bold text-yellow-500">小钱罐 💰</h1>
        <p class="mt-2 text-gray-500">快来记录你的每一笔财富吧！</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
          <input
            v-model="username"
            id="username"
            type="text"
            required
            class="w-full px-4 py-2 mt-1 text-gray-900 bg-yellow-50 border border-gray-300 rounded-xl focus:ring-yellow-500 focus:border-yellow-500 transition-all"
            placeholder="请输入你的昵称"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="w-full px-4 py-2 mt-1 text-gray-900 bg-yellow-50 border border-gray-300 rounded-xl focus:ring-yellow-500 focus:border-yellow-500 transition-all"
            placeholder="请输入密码"
          />
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-center text-red-800 bg-red-100 rounded-lg">
          {{ errorMessage }}
        </div>

        <div>
          <button
            type="submit"
            class="w-full py-3 font-bold text-white bg-yellow-400 rounded-xl hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transform hover:translate-y-[-2px] transition-all duration-200"
          >
            登 录
          </button>
        </div>
      </form>
      <div class="text-sm text-center text-gray-600 pt-4">
        还没有账户？
        <RouterLink :to="{ name: 'register' }" class="font-medium text-orange-500 hover:underline">
          立即注册
        </RouterLink>
      </div>
    </div>
  </div>
</template>
