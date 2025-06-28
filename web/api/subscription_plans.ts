import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type { SubscriptionPlan, SubscriptionPlansResponse } from '~/types/subscription_plan'

export class SubscriptionPlansApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async list(): Promise<ApiResponse<SubscriptionPlansResponse>> {
    return this.http.get<SubscriptionPlansResponse>('/subscription-plans/')
  }

  async get(id: string): Promise<ApiResponse<SubscriptionPlan>> {
    return this.http.get<SubscriptionPlan>(`/subscription-plans/${id}/`)
  }
}