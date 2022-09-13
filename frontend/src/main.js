import Vue from 'vue'
import App from './App2.vue'
// import App from './插槽.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false

Vue.directive('color', function (el, binding) {
  el.style.color = binding.value
})


import axios from 'axios'
import router from './router'
import store from './store'
Vue.prototype.$axios = axios
//由于axios不是vue的插件，不能使用Vue.use(),要通过控制原型链的方式来引入

Vue.use(ElementUI)


new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
