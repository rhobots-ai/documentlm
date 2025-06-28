import type { ApiResponse } from './http'
import { HttpClient } from './http'
import type {ConversationNote} from "~/types/conversation_note";

export interface CreateNoteRequest {
  conversation: string
  content: string
  type: string
}

export class ConversationNotesApi {
  private http: HttpClient

  constructor() {
    this.http = new HttpClient('/api')
  }

  async create(request: CreateNoteRequest): Promise<ApiResponse<ConversationNote>> {
    return this.http.post<ConversationNote>(`/conversation-notes/`, request)
  }

  async list(queryParams?: Record<string, string | number>): Promise<ApiResponse<ConversationNote[]>> {
    return this.http.get<ConversationNote[]>(`/conversation-notes/`, queryParams)
  }

  async update(noteId: string, request: CreateNoteRequest): Promise<ApiResponse<ConversationNote>> {
    return this.http.patch<ConversationNote>(`/conversation-notes/${noteId}/`, request)
  }

  async delete(noteId: string): Promise<ApiResponse<void>> {
    return this.http.delete(`/conversation-notes/${noteId}/`)
  }
}