import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type { Wallet, WalletTransaction } from '~/types/wallet'
import type {Message} from "~/types/message";

export class MessageApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async upvote(id: string): Promise<ApiResponse<Message[]>> {
    return this.http.patch<Message>(`/messages/${id}/upvote/`)
  }

  async downvote(id: string): Promise<ApiResponse<Message[]>> {
    return this.http.patch<Message>(`/messages/${id}/downvote/`)
  }
}