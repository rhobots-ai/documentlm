import type {MindmapNode} from "~/types/mindmap";
import type {Citation} from "~/types/citation";

export type MessageRole = 'user' | 'agent' | 'system';

export type ReasoningType = 'simple' | 'complex' | 'react' | 'rewoo';

export interface Message {
  id: string;
  created_at: string;
  conversation_id: string;
  sender_id?: string | null
  role: MessageRole;
  content: string;
  raw_content?: string | null;
  citation?: Citation[];
  citation_type: 'highlight' | 'inline';
  reasoning_type: ReasoningType;
  reason_content?: string | null;
  mindmap?: MindmapNode | null;
  is_upvote?: boolean;
}
