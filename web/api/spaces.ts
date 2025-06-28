import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type {Space} from "~/types/space";

export interface CreateSpaceRequest {
  name: string
  description: string
  icon: string
}

export class SpacesApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(request: CreateSpaceRequest): Promise<ApiResponse<Space>> {
    return this.http.post<Space>('/spaces/', request)
  }

  async get(id: string): Promise<ApiResponse<Space>> {
    return this.http.get<Space>(`/spaces/${id}/`, {}, false, false)
  }

  async list(): Promise<ApiResponse<Space[]>> {
    return this.http.get<Space[]>('/spaces/')
  }

  async join(id: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/spaces/${id}/join/`, {})
  }

  async leave(id: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/spaces/${id}/leave/`, {})
  }

  async delete(id: string): Promise<ApiResponse<void>> {
    return this.http.delete(`/spaces/${id}/`)
  }
}