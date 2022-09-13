import request from '@/utils/request.js'

export function CashCount(){
  return request.get('/cash_count')
}

export function CashBalance(){
  return request.get('/cash_balance/')
}

export function CashCountUpdate(data){
  return request.post('/cash_count/',data)
}
