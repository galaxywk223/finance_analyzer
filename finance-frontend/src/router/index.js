// src/router/index.js (修正路由守卫)
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// --- 所有的 import 保持不变 ---
import MainLayout from '../layouts/MainLayout.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import AdviceView from '../views/AdviceView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/app',
    component: MainLayout,
    children: [
      { path: '/dashboard', name: 'dashboard', component: DashboardView },
      { path: '/transactions', name: 'transactions', component: TransactionsView },
      { path: '/advice', name: 'advice', component: AdviceView },
      { path: '/categories', name: 'categories', component: CategoriesView },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// --- 修正这里的路由守卫 ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const publicPages = ['login', 'register'] // 定义哪些页面是公开的
  const authRequired = !publicPages.includes(to.name) // 判断要去的页面是否需要登录

  // 如果页面需要登录，而用户没有登录
  if (authRequired && !authStore.isAuthenticated) {
    // 就把他送到登录页
    return next({ name: 'login' })
  }

  // 其他情况一律放行
  next()
})

export default router
