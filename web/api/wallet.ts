import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type { Wallet, WalletTransaction } from '~/types/wallet'

export class WalletApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async getWallet(): Promise<ApiResponse<Wallet>> {
    return this.http.get<Wallet>('/wallet/')
  }

  async getTransactions(id: string): Promise<ApiResponse<WalletTransaction[]>> {
    return this.http.get<WalletTransaction[]>(`/wallet/${id}/transactions/`)
  }
}