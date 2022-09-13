import { getGoodBalanceListAPI } from '@/api/GoodBalanceListAPI.js'

export default{
  state:{
    GoodBalance :[]
  },
  mutations:{
    async initGoodBalanceList() { 
      const {  data: { results: res }} = await getGoodBalanceListAPI()
      this.state.GoodBalance = res
    }
  }
}