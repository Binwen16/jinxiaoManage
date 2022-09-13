import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GoodsCount from '../views/GoodCount.vue'
import addGoodsCount from '@/components/addGoodCount.vue'

Vue.use(VueRouter)

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/goodcount',
    name: 'goodcount',
    component: GoodsCount,
  },
  
  {
    path: '/addgood',
    name: 'addgood',
    component: () => import('@/components/addGood.vue'),
  },
  
  {
    path: '/addgoodcount',
    name: 'addgoodcount',
    component: addGoodsCount,
  },
  
  {
    path: '/addcashcount',
    name: 'addcashcount',
    component: () => import('@/components/addCashCount.vue'),
  },
  {
    path: '/goodbalance',
    name: 'goodbalance',
    component: () => import('@/views/Goodbalance.vue'),
  },

  {
    path: '/cashcount',
    name: 'cashcount',
    component: () => import('@/views/CashCount.vue'),
  },
  {
    path: '/sale',
    name: 'sale',
    component: () => import('@/views/SaleCrate.vue'),
  },
  {
    path: '/salelist',
    name: 'salelist',
    component: () => import('@/views/SaleList.vue'),
  },

  {
    path: '/cashcount',
    name: 'cashcount',
    component: () => import('@/views/CashCount.vue'),
  },


  {
    path: '/cashbalance',
    name: 'cashbalance',
    component: () => import('@/views/CashBalance.vue'),
  },
]

const router = new VueRouter({
  routes,
})

export default router
