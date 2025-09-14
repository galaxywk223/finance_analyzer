<script setup>
import { ref, onMounted, defineProps, defineEmits } from 'vue'
import apiClient from '@/services/api'

// 定义组件的 props 和 emits
const props = defineProps({
  show: Boolean, // 用于控制模态框显示与否
})
const emit = defineEmits(['close', 'transaction-added']) // 定义 'close' 和 'transaction-added' 事件

// 表单数据
const transactionType = ref('expense') // 'expense' or 'income'
const amount = ref('')
const transactionDate = ref(new Date().toISOString().slice(0, 10)) // 默认为今天
const categoryId = ref('')
const notes = ref('')

// 其他状态
const categories = ref([])
const errorMessage = ref('')
const isLoading = ref(false)

// 获取所有分类
const fetchCategories = async () => {
  try {
    const response = await apiClient.get('/categories')
    categories.value = response.data
    // 默认选中第一个分类
    if (categories.value.length > 0) {
      categoryId.value = categories.value[0].id
    }
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 提交表单
const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''

  if (!amount.value || !transactionDate.value) {
    errorMessage.value = '金额和日期不能为空！'
    isLoading.value = false
    return
  }
  if (transactionType.value === 'expense' && !categoryId.value) {
    errorMessage.value = '请选择一个支出分类！'
    isLoading.value = false
    return
  }

  const payload = {
    amount: amount.value,
    type: transactionType.value,
    transaction_date: transactionDate.value,
    notes: notes.value,
    category_id: transactionType.value === 'expense' ? categoryId.value : null,
  }

  try {
    await apiClient.post('/transactions', payload)
    // 成功后，触发 'transaction-added' 事件并关闭模态框
    emit('transaction-added')
    emit('close')
  } catch (error) {
    console.error('创建交易失败:', error)
    errorMessage.value = error.response?.data?.error || '发生未知错误'
  } finally {
    isLoading.value = false
  }
}

// 当组件挂载时，获取分类
onMounted(fetchCategories)
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center"
    @click.self="emit('close')"
  >
    <div
      class="bg-white w-full max-w-md p-8 rounded-2xl shadow-xl space-y-6 transform transition-all"
    >
      <h2 class="text-2xl font-bold text-center text-gray-800">记一笔新账 ✏️</h2>

      <div class="grid grid-cols-2 gap-4">
        <button
          @click="transactionType = 'expense'"
          :class="[
            'py-3 rounded-lg font-semibold transition-colors',
            transactionType === 'expense'
              ? 'bg-red-500 text-white shadow-md'
              : 'bg-gray-100 text-gray-600',
          ]"
        >
          支出 💸
        </button>
        <button
          @click="transactionType = 'income'"
          :class="[
            'py-3 rounded-lg font-semibold transition-colors',
            transactionType === 'income'
              ? 'bg-green-500 text-white shadow-md'
              : 'bg-gray-100 text-gray-600',
          ]"
        >
          收入 🤑
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="amount" class="text-sm font-medium text-gray-700">金额 (¥)</label>
          <input
            type="number"
            step="0.01"
            v-model="amount"
            id="amount"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          />
        </div>

        <div v-if="transactionType === 'expense'">
          <label for="category" class="text-sm font-medium text-gray-700">分类</label>
          <select
            v-model="categoryId"
            id="category"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          >
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>

        <div>
          <label for="date" class="text-sm font-medium text-gray-700">日期</label>
          <input
            type="date"
            v-model="transactionDate"
            id="date"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          />
        </div>

        <div>
          <label for="notes" class="text-sm font-medium text-gray-700">备注 (可选)</label>
          <textarea
            v-model="notes"
            id="notes"
            rows="2"
            class="w-full mt-1 p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
          ></textarea>
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-center text-red-800 bg-red-100 rounded-lg">
          {{ errorMessage }}
        </div>

        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="emit('close')"
            class="px-6 py-3 font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="px-6 py-3 font-semibold text-white bg-orange-500 rounded-lg hover:bg-orange-600 disabled:opacity-50"
          >
            {{ isLoading ? '保存中...' : '保存' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
