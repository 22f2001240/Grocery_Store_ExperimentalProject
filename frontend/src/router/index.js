import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import AdminLogin from '@/components/AdminLogin.vue'
import UserLogin from '@/components/UserLogin.vue'
import ManagerLogin from '@/components/ManagerLogin.vue'
import UserSignup from '@/components/UserSignup.vue'
import ManagerSignup from '@/components/ManagerSignup.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import CreateCategory from '@/components/CreateCategory.vue'
import EditCategory from '@/components/EditCategory.vue'
import ManagerDashboard from '@/components/ManagerDashboard.vue'
import EditProduct from '@/components/EditProduct.vue'
import UserDashboard from '@/components/UserDashboard.vue'
import CustomerCart from '@/components/CustomerCart.vue'
import CustomerOrders from '@/components/CustomerOrders.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin-login',
      name: 'admin-login',
      component: AdminLogin,
    },
    {
      path: '/user-login',
      name: 'user-login',
      component: UserLogin,
    },
    {
      path: '/manager-login',
      name: 'manager-login',
      component: ManagerLogin,
    },
    {
      path: '/user-signup',
      name: 'user-signup',
      component: UserSignup,
    },
    {
      path: '/manager-signup',
      name: 'manager-signup',
      component: ManagerSignup,
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard,
    },
    {
      path: '/create-category',
      name: 'create-category',
      component: CreateCategory,
    },
    {
      path: '/edit-category/:id',
      name: 'edit-category',
      component: EditCategory,
    },
    {
      path: '/manager-dashboard',
      name: 'manager-dashboard',
      component: ManagerDashboard,
    },
    {
      path: '/edit-product/:id',
      name: 'edit-product',
      component: EditProduct,
    },
    {
      path: '/user-dashboard',
      name: 'user-dashboard',
      component: UserDashboard,
    },
    {
      path: '/customer-cart',
      name: 'customer-cart',
      component: CustomerCart,
    },
    {
      path: '/customer-orders',
      name: 'customer-orders',
      component: CustomerOrders,
    }
  ],
})

export default router
