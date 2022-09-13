import request from '@/utils/request.js'

export function getStaff(){
  return request.get('/staff/')
}