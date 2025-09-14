<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '@/services/api'

const categories = ref([])
const isLoading = ref(true)
const newCategoryName = ref('')
const editingCategory = ref(null) // 用于存储正在编辑的分类对象

// 计算属性，区分系统分类和用户自定义分类
const systemCategories = computed(() => categories.value.filter((c) => !c.is_custom))
const userCategories = computed(() => categories.value.filter((c) => c.is_custom))

// 获取所有分类
const fetchCategories = async () => {
  isLoading.value = true
  try {
    const response = await apiClient.get('/categories')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类失败:', error)
  } finally {
    isLoading.value = false
  }
}

// 添加新分类
const addCategory = async () => {
  if (!newCategoryName.value.trim()) return
  try {
    await apiClient.post('/categories', { name: newCategoryName.value })
    newCategoryName.value = '' // 清空输入框
    fetchCategories() // 重新加载列表
  } catch (error) {
    alert('添加分类失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

// 删除分类
const deleteCategory = async (category) => {
  if (confirm(`确定要删除分类 "${category.name}" 吗？所有使用该分类的交易将变为“未分类”。`)) {
    try {
      await apiClient.delete(`/categories/${category.id}`)
      fetchCategories() // 重新加载列表
    } catch (error) {
      alert('删除分类失败: ' + (error.response?.data?.error || '未知错误'))
    }
  }
}

// 开始编辑分类
const startEditing = (category) => {
  // 创建一个副本进行编辑，避免直接修改原始数据
  editingCategory.value = { ...category }
}

// 保存编辑
const saveCategory = async () => {
  if (!editingCategory.value || !editingCategory.value.name.trim()) return
  try {
    await apiClient.put(`/categories/${editingCategory.value.id}`, {
      name: editingCategory.value.name,
    })
    editingCategory.value = null // 退出编辑模式
    fetchCategories() // 重新加载列表
  } catch (error) {
    alert('更新分类失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

onMounted(fetchCategories)
</script>

<template>
  <div class="space-y-8">
    <header>
      <h1 class="text-3xl font-bold text-gray-800">分类管理 🏷️</h1>
      <p class="mt-2 text-gray-500">管理你的自定义消费类别。</p>
    </header>

    <div class="p-6 bg-white rounded-2xl shadow-md">
      <form @submit.prevent="addCategory" class="flex items-center gap-4">
        <input
          v-model="newCategoryName"
          type="text"
          placeholder="输入新的分类名称"
          class="flex-grow p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-orange-500 focus:border-orange-500"
        />
        <button
          type="submit"
          class="px-6 py-3 font-semibold text-white bg-orange-500 rounded-lg hover:bg-orange-600"
        >
          添加
        </button>
      </form>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="p-6 bg-white rounded-2xl shadow-md space-y-4">
        <h2 class="text-xl font-bold text-gray-700">我的分类</h2>
        <ul class="divide-y divide-gray-100">
          <li
            v-for="cat in userCategories"
            :key="cat.id"
            class="py-3 flex items-center justify-between"
          >
            <div v-if="editingCategory && editingCategory.id === cat.id" class="flex-grow">
              <input
                v-model="editingCategory.name"
                @keyup.enter="saveCategory"
                @keyup.esc="editingCategory = null"
                class="p-2 border rounded-md w-full"
              />
            </div>
            <span v-else class="text-gray-800">{{ cat.name }}</span>

            <div class="space-x-2 flex-shrink-0 ml-4">
              <template v-if="editingCategory && editingCategory.id === cat.id">
                <button @click="saveCategory" class="text-green-500 hover:text-green-700">✓</button>
                <button @click="editingCategory = null" class="text-gray-500 hover:text-gray-700">
                  ✗
                </button>
              </template>
              <template v-else>
                <button @click="startEditing(cat)" class="text-blue-500 hover:text-blue-700">
                  ✏️
                </button>
                <button @click="deleteCategory(cat)" class="text-red-500 hover:text-red-700">
                  🗑️
                </button>
              </template>
            </div>
          </li>
        </ul>
      </div>
      <div class="p-6 bg-gray-50 rounded-2xl shadow-inner space-y-4">
        <h2 class="text-xl font-bold text-gray-600">系统分类</h2>
        <div class="flex flex-wrap gap-3">
          <span
            v-for="cat in systemCategories"
            :key="cat.id"
            class="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm"
          >
            {{ cat.name }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
