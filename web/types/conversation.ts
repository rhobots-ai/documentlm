import type {DataSource} from "~/types/data_source";
import type {Message} from "~/types/message";
import type {ConversationNote} from "~/types/conversation_note";
import type {Space} from "~/types/space";

export interface Conversation {
  id: string
  name: string
  space: Space
  is_public: boolean
  data_sources: DataSource[]
  created_by: string | null
  created_at: string
  messages: Message[]
  last_message_at: string | null
  notes: ConversationNote[]
  message_count: number | null
}