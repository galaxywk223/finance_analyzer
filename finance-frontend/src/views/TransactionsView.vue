<script setup>
import { ref, onMounted, watch } from 'vue'
import apiClient from '@/services/api'
import EditTransactionModal from '@/components/EditTransactionModal.vue' // 1. 导入编辑模态框

const transactions = ref([])
const pagination = ref({})
const isLoading = ref(true)
const errorMessage = ref('')
const currentPage = ref(1)

// 2. 编辑模态框相关状态
const showEditModal = ref(false)
const editingTransactionId = ref(null)

const fetchTransactions = async (page) => {
  isLoading.value = true
  try {
    const response = await apiClient.get('/transactions', { params: { page, per_page: 10 } })
    transactions.value = response.data.items
    const { items, ...paginationData } = response.data
    pagination.value = paginationData
  } catch (error) {
    errorMessage.value = '获取交易记录失败'
  } finally {
    isLoading.value = false
  }
}

// 3. 打开编辑模态框
const openEditModal = (id) => {
  editingTransactionId.value = id
  showEditModal.value = true
}

// 4. 删除交易
const deleteTransaction = async (id) => {
  if (confirm('确定要删除这条交易记录吗？此操作无法撤销。')) {
    try {
      await apiClient.delete(`/transactions/${id}`)
      fetchTransactions(currentPage.value) // 删除成功后刷新列表
    } catch (error) {
      alert('删除失败: ' + (error.response?.data?.error || '未知错误'))
    }
  }
}

watch(currentPage, (newPage) => {
  fetchTransactions(newPage)
})

onMounted(() => {
  fetchTransactions(currentPage.value)
})
</script>

<template>
  <div class="space-y-6">
    <header>
      <h1 class="text-3xl font-bold text-gray-800">交易记录 🧾</h1>
      <p class="mt-2 text-gray-500">这里是你的每一笔花销和收入～</p>
    </header>

    <div v-if="isLoading" class="text-center text-gray-500 py-10">
      <p>正在加载交易记录... 💨</p>
    </div>
    <div v-else-if="errorMessage" class="p-4 text-center text-red-700 bg-red-100 rounded-lg">
      {{ errorMessage }}
    </div>

    <div v-else-if="transactions.length > 0" class="bg-white p-6 rounded-2xl shadow-md">
      <ul class="divide-y divide-gray-100">
        <li v-for="t in transactions" :key="t.id" class="flex items-center justify-between py-4">
          <div class="flex items-center space-x-4">
            <span
              :class="[
                'flex items-center justify-center w-12 h-12 rounded-full',
                t.type === 'expense' ? 'bg-red-100' : 'bg-green-100',
              ]"
            >
              {{ t.type === 'expense' ? '💸' : '🤑' }}
            </span>
            <div>
              <p class="font-semibold text-gray-800">{{ t.category_name || '收入' }}</p>
              <p class="text-sm text-gray-500">{{ t.transaction_date }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <p
              :class="[
                'font-bold text-lg',
                t.type === 'expense' ? 'text-red-500' : 'text-green-600',
              ]"
            >
              {{ t.type === 'expense' ? '-' : '+' }} ¥{{ t.amount }}
            </p>
            <div class="space-x-2">
              <button
                @click="openEditModal(t.id)"
                class="text-blue-500 hover:text-blue-700 text-xl"
              >
                ✏️
              </button>
              <button
                @click="deleteTransaction(t.id)"
                class="text-red-500 hover:text-red-700 text-xl"
              >
                🗑️
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <div v-else class="text-center text-gray-500 py-10">
      <p>还没有任何交易记录哦，快去记一笔吧！✏️</p>
    </div>

    <div v-if="pagination.total_pages > 1" class="flex justify-center items-center space-x-4 pt-4">
      <button
        @click="currentPage--"
        :disabled="!pagination.has_prev"
        class="px-4 py-2 bg-white rounded-lg shadow-md font-semibold text-gray-700 disabled:opacity-50 hover:bg-gray-50"
      >
        上一页
      </button>
      <span class="text-gray-600"
        >第 {{ pagination.current_page }} 页 / 共 {{ pagination.total_pages }} 页</span
      >
      <button
        @click="currentPage++"
        :disabled="!pagination.has_next"
        class="px-4 py-2 bg-white rounded-lg shadow-md font-semibold text-gray-700 disabled:opacity-50 hover:bg-gray-50"
      >
        下一页
      </button>
    </div>

    <EditTransactionModal
      :show="showEditModal"
      :transaction-id="editingTransactionId"
      @close="showEditModal = false"
      @transaction-updated="
        () => {
          showEditModal = false
          fetchTransactions(currentPage)
        }
      "
    />
  </div>
</template>
