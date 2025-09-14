<script setup>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
import { defineProps } from 'vue'

// Chart.js 必须在使用前注册它需要用到的组件
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

// 定义这个组件接收哪些“道具”(props)
const props = defineProps({
  chartData: {
    type: Object,
    required: true,
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '消费分类',
        },
      },
    }),
  },
})
</script>

<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>
