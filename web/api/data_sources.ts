import type {ApiResponse} from './http'
import {HttpClient} from './http'
import type {CreateDataSourceResponse, DataSource} from '~/types/data_source'


export class DataSourcesApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(files?: FileList, url?: string | null, conversationId?: string | null, spaceId?: string | null): Promise<ApiResponse<CreateDataSourceResponse>> {
    const formData = new FormData();

    if (files) {
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }
    }

    if (url) {
      formData.append('url', url);
    }

    // Add conversation_id to formData if provided
    if (conversationId) {
      formData.append('conversation_id', conversationId);
    }

    // Add space_id to formData if provided
    if (spaceId) {
      formData.append('space_id', spaceId);
    }

    const headers = await this.http.getHeaders()
    delete headers['Content-Type']

    const response = await fetch(this.http.getUrl('/data-sources/'), {
      method: 'POST',
      headers: headers,
      body: formData
    });

    if (!response.ok) {
      if (response.status === 402) {
        return {
          body: await response.json(),
          error: new Error(`Failed to start completion: ${response.status}`),
          ok: false,
          status: 402
        };
      }
      return {
        body: null,
        error: new Error(`Failed to create data source: ${response.status}`),
        ok: false,
        status: response.status
      };
    }

    return {
      body: await response.json(),
      error: null,
      ok: true,
      status: 200
    };
  }

  async get(id: string): Promise<ApiResponse<DataSource>> {
    return this.http.get<DataSource>(`/data-sources/${id}/`)
  }

  async list(): Promise<ApiResponse<DataSource[]>> {
    return this.http.get<DataSource[]>('/data-sources/')
  }

  async delete(id: string): Promise<ApiResponse<void>> {
    return this.http.delete(`/data-sources/${id}/`)
  }
}