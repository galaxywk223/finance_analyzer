<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { defineProps } from 'vue'

// 注册折线图所需的全部组件
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

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
          display: false, // 通常趋势图不需要显示图例
        },
        title: {
          display: true,
          text: '最近30天消费趋势',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    }),
  },
})
</script>

<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
