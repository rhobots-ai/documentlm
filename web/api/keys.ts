import type {ApiResponse} from "~/api/http";
import {HttpClient} from "~/api/http";
import type {ApiKey} from "~/types/api_key";

export interface CreateKeyRequest {
  name: string
  expiryDays: number
}

export class KeysApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async createKey(request: CreateKeyRequest): Promise<ApiResponse<ApiKey>> {
    return this.http.post<ApiKey>('/tokens/create/', request)
  }

  async getKeys(): Promise<ApiResponse<ApiKey[]>> {
    return this.http.get<ApiKey[]>('/keys/')
  }

  async revokeKey(digest: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/keys/${digest}/revoke/`, {})
  }

  async revokeAll(): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/keys/revoke_all/`, {})
  }
}