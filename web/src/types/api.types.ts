/* ============================================
   API TYPES - Tipos para respuestas de API
   ============================================ */

export interface Message {
  id: string;
  role: 'user' | 'bot' | 'info';
  content: string;
  timestamp: Date;
  done?: boolean;
}

export interface NewsItem {
  id: number;
  title: string;
  summary: string;
  content: string;
  category: string;
  post_date: string;
}

export type MessageRole = 'user' | 'bot' | 'info';

export interface SSEEvent {
  content: string;
  type: 'text' | 'error' | 'info';
  done: boolean;
}

/* ============================================
   HISTORY API TYPES - Tipos para historial de conversaciones
   ============================================ */

export interface ConversationRead {
  uuid: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface MessageRead {
  uuid: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: string;
}
