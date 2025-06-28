import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type {Tag, UpdateTagRequest} from "~/types/tag";

export interface CreateTagRequest {
  name: string
  color: string
  parent_id?: string | null
}

export class TagsApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(request: CreateTagRequest): Promise<ApiResponse<Tag>> {
    return this.http.post<Tag>('/tags/', request)
  }
  async update(id: string, request: UpdateTagRequest): Promise<ApiResponse<Tag>> {
    return this.http.patch<Tag>(`/tags/${id}/`, request)
  }

  async get(id: string): Promise<ApiResponse<Tag>> {
    return this.http.get<Tag>(`/tags/${id}/`)
  }

  async list(): Promise<ApiResponse<Tag[]>> {
    return this.http.get<Tag[]>('/tags/', {}, false, false)
  }

  async delete(id: string): Promise<ApiResponse<void>> {
    return this.http.delete(`/tags/${id}/`)
  }
}