import request from '@/utils/request.js'

export function getGoodBalanceListAPI(){
  return request.get('/goods_balance')
}

export function GoodBalancecrate(data){
  return request.post('/goods_balance/',data)
}
