import type {ApiResponse} from './http'
import {HttpClient} from './http'
import type {Subscription, TokenUsage} from "~/types/subscription";

export interface NewSubscriptionRequest {
  plan_id: string
}

export class SubscriptionsApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async getMySubscription(): Promise<ApiResponse<Subscription>> {
    return this.http.get<Subscription>('/subscription/me/')
  }

  async getTokenUsage(): Promise<ApiResponse<TokenUsage>> {
    return this.http.get<Subscription>('/subscription/usage/')
  }

  async create(request: NewSubscriptionRequest): Promise<ApiResponse<Subscription>> {
    return this.http.post<Subscription>('/subscription/new/', request)
  }

  async refresh(request: NewSubscriptionRequest): Promise<ApiResponse<Subscription>> {
    return this.http.get<Subscription>('/subscription/refresh/', request)
  }
}