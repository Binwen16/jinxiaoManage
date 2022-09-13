import request from '@/utils/request.js'

export function GoodsCount(){
  return request.get('/goods_count')
}

export function GoodCountCreat(data){
  return request.post('/goods_count/',data)
}

export function Goods(){
  return request.get('/goods/')
}

