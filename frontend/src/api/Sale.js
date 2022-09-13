import request from '@/utils/request.js'


export function SaleOrder(){
  return request.get('/sales_orders/')
}

export function SaleOrderUpdate(data){
  return request.patch(`/sales_orders/${data.id}/`,data)
}

export function SaleOrderCreat(data){
  return request.post('/sales_orders/',data)
}

// export function userDestroy(data) {
//   return request({ url: `/users/${data.id}/`, method: 'delete', data })
// }