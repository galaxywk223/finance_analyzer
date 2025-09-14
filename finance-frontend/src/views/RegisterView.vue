<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import apiClient from '@/services/api'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const router = useRouter()

const handleRegister = async () => {
  // 客户端校验
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致！'
    return
  }
  if (password.value.length < 6) {
    errorMessage.value = '密码长度不能少于6位！'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await apiClient.post('/register', {
      username: username.value,
      password: password.value,
    })

    successMessage.value = '🎉 注册成功！即将跳转到登录页面...'

    // 注册成功后，等待2秒，然后跳转到登录页
    setTimeout(() => {
      router.push({ name: 'login' })
    }, 2000)
  } catch (error) {
    console.error('注册失败:', error)
    errorMessage.value = error.response?.data?.error || '注册失败，请换个用户名试试。'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-yellow-100">
    <div class="w-full max-w-sm p-8 space-y-6 bg-white rounded-3xl shadow-lg">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-yellow-500">加入小钱罐 💰</h1>
        <p class="mt-2 text-gray-500">创建一个新账户吧！</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
          <input
            v-model="username"
            id="username"
            type="text"
            required
            class="w-full px-4 py-2 mt-1 text-gray-900 bg-yellow-50 border border-gray-300 rounded-xl focus:ring-yellow-500 focus:border-yellow-500"
            placeholder="创建你的昵称"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="w-full px-4 py-2 mt-1 text-gray-900 bg-yellow-50 border border-gray-300 rounded-xl focus:ring-yellow-500 focus:border-yellow-500"
            placeholder="至少6位"
          />
        </div>

        <div>
          <label for="confirm-password" class="block text-sm font-medium text-gray-700"
            >确认密码</label
          >
          <input
            v-model="confirmPassword"
            id="confirm-password"
            type="password"
            required
            class="w-full px-4 py-2 mt-1 text-gray-900 bg-yellow-50 border border-gray-300 rounded-xl focus:ring-yellow-500 focus:border-yellow-500"
            placeholder="再次输入密码"
          />
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-center text-red-800 bg-red-100 rounded-lg">
          {{ errorMessage }}
        </div>
        <div
          v-if="successMessage"
          class="p-3 text-sm text-center text-green-800 bg-green-100 rounded-lg"
        >
          {{ successMessage }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 font-bold text-white bg-yellow-400 rounded-xl hover:bg-yellow-500 disabled:opacity-50"
          >
            {{ isLoading ? '注册中...' : '立即注册' }}
          </button>
        </div>
      </form>

      <div class="text-sm text-center text-gray-600">
        已经有账户了？
        <RouterLink :to="{ name: 'login' }" class="font-medium text-orange-500 hover:underline">
          去登录
        </RouterLink>
      </div>
    </div>
  </div>
</template>
