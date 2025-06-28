import type {DataSource} from "~/types/data_source";
import type {Conversation} from "~/types/conversation";

export interface Space {
  id: string
  name: string
  description: string
  icon: string
  members: []
  data_sources: DataSource[]
  conversations: Conversation[]
  joined: boolean
  created_at: string
  updated_at: string
}