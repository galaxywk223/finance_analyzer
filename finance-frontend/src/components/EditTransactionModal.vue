<script setup>
import { ref, onMounted, defineProps, defineEmits, watch } from 'vue'
import apiClient from '@/services/api'

const props = defineProps({
  show: Boolean,
  transactionId: Number, // 接收要编辑的交易ID
})
const emit = defineEmits(['close', 'transaction-updated'])

const formData = ref({})
const categories = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

// 获取所有分类
const fetchCategories = async () => {
  try {
    const response = await apiClient.get('/categories')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 获取指定ID的交易详情
const fetchTransactionDetails = async (id) => {
  if (!id) return
  isLoading.value = true
  try {
    const response = await apiClient.get(`/transactions/${id}`)
    formData.value = response.data
  } catch (error) {
    console.error('获取交易详情失败:', error)
    errorMessage.value = '加载数据失败'
  } finally {
    isLoading.value = false
  }
}

// 监听 transactionId 的变化，当它从父组件传来时，获取数据
watch(
  () => props.transactionId,
  (newId) => {
    if (newId) {
      fetchTransactionDetails(newId)
    }
  },
)

// 提交更新
const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    await apiClient.put(`/transactions/${props.transactionId}`, formData.value)
    emit('transaction-updated')
    emit('close')
  } catch (error) {
    console.error('更新交易失败:', error)
    errorMessage.value = error.response?.data?.error || '更新失败'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchCategories)
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center"
    @click.self="emit('close')"
  >
    <div class="bg-white w-full max-w-md p-8 rounded-2xl shadow-xl space-y-6">
      <h2 class="text-2xl font-bold text-center text-gray-800">编辑交易 ✏️</h2>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="text-sm font-medium text-gray-700">类型</label>
          <div class="grid grid-cols-2 gap-4 mt-1">
            <button
              type="button"
              @click="formData.type = 'expense'"
              :class="[
                'py-3 rounded-lg font-semibold',
                formData.type === 'expense' ? 'bg-red-500 text-white' : 'bg-gray-100',
              ]"
            >
              支出
            </button>
            <button
              type="button"
              @click="formData.type = 'income'"
              :class="[
                'py-3 rounded-lg font-semibold',
                formData.type === 'income' ? 'bg-green-500 text-white' : 'bg-gray-100',
              ]"
            >
              收入
            </button>
          </div>
        </div>
        <div>
          <label for="amount" class="text-sm font-medium text-gray-700">金额 (¥)</label>
          <input
            type="number"
            step="0.01"
            v-model="formData.amount"
            id="amount"
            class="w-full mt-1 p-3 bg-gray-50 border rounded-lg"
          />
        </div>
        <div v-if="formData.type === 'expense'">
          <label for="category" class="text-sm font-medium text-gray-700">分类</label>
          <select
            v-model="formData.category_id"
            id="category"
            class="w-full mt-1 p-3 bg-gray-50 border rounded-lg"
          >
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div>
          <label for="date" class="text-sm font-medium text-gray-700">日期</label>
          <input
            type="date"
            v-model="formData.transaction_date"
            id="date"
            class="w-full mt-1 p-3 bg-gray-50 border rounded-lg"
          />
        </div>
        <div>
          <label for="notes" class="text-sm font-medium text-gray-700">备注</label>
          <textarea
            v-model="formData.notes"
            id="notes"
            rows="2"
            class="w-full mt-1 p-3 bg-gray-50 border rounded-lg"
          ></textarea>
        </div>
        <div v-if="errorMessage" class="p-3 text-sm text-center text-red-800 bg-red-100 rounded-lg">
          {{ errorMessage }}
        </div>
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="emit('close')"
            class="px-6 py-3 font-semibold text-gray-700 bg-gray-100 rounded-lg"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="px-6 py-3 font-semibold text-white bg-orange-500 rounded-lg"
          >
            {{ isLoading ? '保存中...' : '保存' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
