<script setup>
import { ref } from 'vue'
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AddTransactionModal from '@/components/AddTransactionModal.vue' // 1. 导入模态框组件

const authStore = useAuthStore()
const router = useRouter()

const showModal = ref(false) // 2. 控制模态框的显示状态

// 3. 当交易添加成功后，刷新当前页面以显示最新数据
const onTransactionAdded = () => {
  // 通过给路由 push 一个空对象并带上 key 来强制刷新当前组件
  router.push({ path: router.currentRoute.value.path, query: { t: Date.now() } })
}
</script>

<template>
  <div class="flex h-screen bg-orange-50">
    <aside class="w-64 flex-shrink-0 bg-white shadow-lg p-6">
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-orange-500">小钱罐 💰</h1>
      </div>
      <nav class="space-y-4">
        <RouterLink
          to="/dashboard"
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-orange-100 hover:text-orange-600 transition-colors"
          active-class="bg-orange-200 text-orange-700 font-bold"
        >
          <span class="mr-3">📊</span>仪表盘
        </RouterLink>
        <RouterLink
          to="/transactions"
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-orange-100 hover:text-orange-600 transition-colors"
          active-class="bg-orange-200 text-orange-700 font-bold"
        >
          <span class="mr-3">🧾</span>交易记录
        </RouterLink>
        <RouterLink
          to="/advice"
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-orange-100 hover:text-orange-600 transition-colors"
          active-class="bg-orange-200 text-orange-700 font-bold"
        >
          <span class="mr-3">💡</span>
          AI 建议
        </RouterLink>
        <RouterLink
          to="/categories"
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-orange-100 hover:text-orange-600 transition-colors"
          active-class="bg-orange-200 text-orange-700 font-bold"
        >
          <span class="mr-3">🏷️</span>
          分类管理
        </RouterLink>
      </nav>
      <div class="absolute bottom-6 left-6">
        <button
          @click="authStore.logout()"
          class="flex items-center w-full px-4 py-3 text-gray-700 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
        >
          <span class="mr-3">👋</span>退出登录
        </button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-8 relative">
      <button
        @click="showModal = true"
        class="fixed bottom-10 right-10 z-30 w-16 h-16 bg-orange-500 text-white rounded-full shadow-lg flex items-center justify-center text-3xl font-bold transform hover:scale-110 transition-transform"
      >
        +
      </button>
      <RouterView />
    </main>

    <AddTransactionModal
      :show="showModal"
      @close="showModal = false"
      @transaction-added="onTransactionAdded"
    />
  </div>
</template>
