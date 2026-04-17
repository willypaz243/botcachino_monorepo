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
