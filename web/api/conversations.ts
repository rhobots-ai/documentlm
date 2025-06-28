import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type { Conversation } from '~/types/conversation'
import type {ReasoningType} from "~/types/message";

export interface CreateConversationRequest {
  name: string
  space_id?: string | null
  is_public?: boolean
  data_sources?: string[]
}

export class ConversationsApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(request: CreateConversationRequest): Promise<ApiResponse<Conversation>> {
    return this.http.post<Conversation>('/conversations/', request)
  }

  async get(id: string): Promise<ApiResponse<Conversation>> {
    return this.http.get<Conversation>(`/conversations/${id}/`)
  }

  async list(nextPage): Promise<ApiResponse<Conversation[]>> {
    const url = nextPage || '/conversations/'
    return this.http.get<Conversation[]>(url, null, nextPage != null)
  }

  async delete(id: string): Promise<ApiResponse<void>> {
    return this.http.delete(`/conversations/${id}/`)
  }

  async addDataSource(id: string, dataSourceId: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/conversations/${id}/data-sources/`, {
      data_source_id: dataSourceId
    })
  }

  async removeDataSource(id: string, dataSourceId: string): Promise<ApiResponse<void>> {
    return this.http.delete<void>(`/conversations/${id}/data-sources/${dataSourceId}/`)
  }

  async sendMessage(id: string, message: string, citation: string, reasoning_type: ReasoningType): Promise<ApiResponse> {
    const baseUrl = this.http.getUrl(`/conversations/${id}/completion/?stream=true`)
    const headers = await this.http.getHeaders()
    let ok = false
    let status = 0

    // First make the POST request to start the completion
    const response = await fetch(baseUrl, {
      method: 'POST',
      headers: {
        ...headers,
        'Accept': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      },
      body: JSON.stringify({ message, citation, reasoning_type })
    })

    ok = response.ok
    status = response.status

    if (!response.ok) {
      return {
        ok,
        status,
        body: await response.json(),
        error: new Error(`Failed to start completion: ${response.status}`)
      }
    }

    return {
      ok,
      status,
      body: response.body.getReader()
    }
  }

  async rename(id: string, name: string): Promise<ApiResponse<void>> {
    return this.http.patch<void>(`/conversations/${id}/`, { name })
  }
}