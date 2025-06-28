import type {Conversation} from "~/types/conversation";

export interface DataSource {
  id: string
  title: string
  file: string
  type: string
  size: number
  status: 'created' | 'processing' | 'indexed' | 'errored';
  created_at: string
  created_by: string | null
}

export interface CreateDataSourceResponse {
  conversation: Conversation
  message: string
}