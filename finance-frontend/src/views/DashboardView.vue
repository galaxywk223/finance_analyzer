<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import PieChart from '@/components/PieChart.vue'
import LineChart from '@/components/LineChart.vue' // 1. 导入折线图组件

const authStore = useAuthStore()
const summaryData = ref(null)
const isLoading = ref(true)
const errorMessage = ref('')

// 饼图数据 (保持不变)
const pieChartData = computed(() => {
  if (!summaryData.value || !summaryData.value.category_breakdown.length) return null
  return {
    labels: summaryData.value.category_breakdown.map((item) => item.category),
    datasets: [
      {
        backgroundColor: [
          '#FFDDC1',
          '#FFAB91',
          '#FF8A65',
          '#FF7043',
          '#FF5722',
          '#F4511E',
          '#E64A19',
        ],
        data: summaryData.value.category_breakdown.map((item) => item.total),
      },
    ],
  }
})

// 2. 新增：为折线图格式化数据
const lineChartData = computed(() => {
  if (!summaryData.value || !summaryData.value.daily_trend_last_30_days.length) return null

  // 我们需要一个完整的30天日期标签，即使那天没有消费
  const labels = [...Array(30).keys()].map((i) => {
    const d = new Date()
    d.setDate(d.getDate() - 29 + i)
    return d.toLocaleDateString('sv-SE').slice(5) // 格式化为 MM-DD
  })

  const dataPoints = summaryData.value.daily_trend_last_30_days
  const data = labels.map((label) => {
    const dateToFind = `2025-${label}` // 假设年份，以匹配后端数据格式
    const found = dataPoints.find((p) => p.date.endsWith(label))
    return found ? found.total : 0
  })

  return {
    labels: labels,
    datasets: [
      {
        label: '每日消费',
        borderColor: '#F97316', // 橙色线条
        backgroundColor: '#FFF7ED', // 橙色区域填充
        tension: 0.3, // 让线条更平滑
        fill: true,
        data: data,
      },
    ],
  }
})

const fetchDashboardSummary = async () => {
  try {
    const response = await apiClient.get('/dashboard/summary')
    summaryData.value = response.data
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
    errorMessage.value = '获取数据失败，请稍后刷新重试。'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDashboardSummary()
})
</script>

<template>
  <div class="min-h-screen bg-orange-50 p-6">
    <header class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-orange-500">我的小钱罐 dashboard</h1>
      <button
        @click="authStore.logout()"
        class="px-4 py-2 font-bold text-white bg-orange-400 rounded-full hover:bg-orange-500 transition-all transform hover:scale-105"
      >
        退出登录 👋
      </button>
    </header>

    <div v-if="isLoading" class="text-center text-gray-500">
      <p>正在努力加载数据中... 💨</p>
    </div>
    <div v-else-if="errorMessage" class="p-4 text-center text-red-700 bg-red-100 rounded-lg">
      {{ errorMessage }}
    </div>

    <div v-else-if="summaryData" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          class="p-6 bg-green-100 rounded-2xl shadow-md text-center transform hover:-translate-y-1 transition-transform"
        >
          <p class="text-lg font-semibold text-green-700">本月收入 🤑</p>
          <p class="text-4xl font-bold text-green-800 mt-2">
            ¥ {{ summaryData.current_month_summary.income }}
          </p>
        </div>
        <div
          class="p-6 bg-red-100 rounded-2xl shadow-md text-center transform hover:-translate-y-1 transition-transform"
        >
          <p class="text-lg font-semibold text-red-700">本月支出 💸</p>
          <p class="text-4xl font-bold text-red-800 mt-2">
            ¥ {{ summaryData.current_month_summary.expense }}
          </p>
        </div>
        <div
          class="p-6 bg-blue-100 rounded-2xl shadow-md text-center transform hover:-translate-y-1 transition-transform"
        >
          <p class="text-lg font-semibold text-blue-700">本月结余 🏦</p>
          <p class="text-4xl font-bold text-blue-800 mt-2">
            ¥ {{ summaryData.current_month_summary.balance }}
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div class="lg:col-span-2 p-6 bg-white rounded-2xl shadow-md">
          <PieChart v-if="pieChartData" :chart-data="pieChartData" />
          <div v-else class="flex items-center justify-center h-full text-gray-500">
            <p>暂无本月消费数据</p>
          </div>
        </div>
        <div class="lg:col-span-3 p-6 bg-white rounded-2xl shadow-md">
          <LineChart v-if="lineChartData" :chart-data="lineChartData" style="height: 300px" />
          <div v-else class="flex items-center justify-center h-full text-gray-500">
            <p>暂无近期消费数据</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
