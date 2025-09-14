<script setup>
import { ref } from 'vue'
import apiClient from '@/services/api'

// 设置默认日期范围为最近30天
const today = new Date()
const thirtyDaysAgo = new Date()
thirtyDaysAgo.setDate(today.getDate() - 30)

const startDate = ref(thirtyDaysAgo.toISOString().slice(0, 10))
const endDate = ref(today.toISOString().slice(0, 10))

// 响应式状态
const advice = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// 获取AI建议的方法
const getAdvice = async () => {
  isLoading.value = true
  errorMessage.value = ''
  advice.value = ''

  try {
    const response = await apiClient.post('/advice', {
      start_date: startDate.value,
      end_date: endDate.value,
    })
    advice.value = response.data.advice
  } catch (error) {
    console.error('获取AI建议失败:', error)
    errorMessage.value = error.response?.data?.error || '生成建议时出错，请稍后再试。'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="space-y-8">
    <header>
      <h1 class="text-3xl font-bold text-gray-800">AI 财务顾问 🤖</h1>
      <p class="mt-2 text-gray-500">选择一个时间范围，让AI分析你的消费并提供建议吧！</p>
    </header>

    <div class="p-6 bg-white rounded-2xl shadow-md">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
        <div>
          <label for="start-date" class="block text-sm font-medium text-gray-700">开始日期</label>
          <input
            type="date"
            v-model="startDate"
            id="start-date"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          />
        </div>
        <div>
          <label for="end-date" class="block text-sm font-medium text-gray-700">结束日期</label>
          <input
            type="date"
            v-model="endDate"
            id="end-date"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          />
        </div>
        <button
          @click="getAdvice"
          :disabled="isLoading"
          class="w-full py-3 font-semibold text-white bg-orange-500 rounded-lg hover:bg-orange-600 disabled:opacity-50 transition-colors shadow hover:shadow-lg"
        >
          {{ isLoading ? '分析中...' : '生成建议' }}
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="text-center text-gray-500 py-10">
      <p>AI 顾问正在思考中，请稍候... 🤔</p>
    </div>

    <div v-if="errorMessage" class="p-4 text-center text-red-700 bg-red-100 rounded-lg">
      {{ errorMessage }}
    </div>

    <div v-if="advice" class="p-6 bg-white rounded-2xl shadow-md space-y-4">
      <p class="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">{{ advice }}</p>
    </div>
  </div>
</template>
