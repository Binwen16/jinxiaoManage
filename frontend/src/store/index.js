import Vue from 'vue'
import Vuex from 'vuex'
import tab from './tab'
import getGoodBalance from './getGoodBalance.js'


Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tab,
    getGoodBalance
  }
})
