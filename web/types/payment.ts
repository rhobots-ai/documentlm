export interface Payment {
  id: string
  order_id: string
  amount: number
  currency: string
  status: string
  created_at: string
}

export interface UpdateStatusRequest {
  order_id: string
  payment_id: string
  signature: string
}