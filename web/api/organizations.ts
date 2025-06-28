import type {ApiResponse} from "~/api/http";
import {HttpClient} from "~/api/http";
import type {Organization} from "~/types/organization";


export interface CreateOrganizationRequest {
  name: string
  slug: string
}

export class OrganizationsApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient()
  }

  async getOrganization(id: string): Promise<ApiResponse<Organization>> {
    return this.http.get<Organization>(`/organizations/${id}/`)
  }

  async getOrganizationBySlug(slug: string): Promise<ApiResponse<any>> {
    return this.http.get<Organization>(`/organizations/`, {slug}, false, false)
  }

  async createOrganization(request: CreateOrganizationRequest): Promise<ApiResponse<Organization>> {
    return this.http.post<Organization>('/organizations/', request)
  }

  async getMembers(id: string): Promise<ApiResponse<any[]>> {
    return this.http.get<any[]>(`/organizations/${id}/members/`)
  }

  async inviteMember(id: string, email: string, role: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/organizations/${id}/invite/`, {email, role})
  }

  async removeMember(id: string, userId: string): Promise<ApiResponse<void>> {
    return this.http.post<void>(`/organizations/${id}/members/${userId}/remove/`, {})
  }
}