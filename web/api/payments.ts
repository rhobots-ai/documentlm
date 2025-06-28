import type {ApiResponse} from './http'
import {HttpClient} from './http'
import type {Payment} from "~/types/payment";

export interface CreatePaymentRequest {
  amount: number
}

export class PaymentsApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(request: CreatePaymentRequest): Promise<ApiResponse<Payment>> {
    return this.http.post<Payment>('/payments/', request)
  }

  async updateStatus(request: UpdateStatusRequest): Promise<ApiResponse<Payment>> {
    return this.http.post<Payment>('/payments/update-status/', request)
  }

  async get(id: string): Promise<ApiResponse<Payment>> {
    return this.http.get<Payment>(`/payments/${id}/`)
  }

  async list(): Promise<ApiResponse<Payment[]>> {
    return this.http.get<Payment[]>('/payments/')
  }
}