/* ============================================
   HOOKS TYPES - Tipos para hooks reutilizables
   ============================================ */

import type { Message as MessageType, NewsItem, SSEEvent } from './api.types';

export type Message = MessageType;
export type { SSEEvent };

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  isOnline: boolean;
}

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  isOnline: boolean;
  sendMessage: (content: string) => void;
  clearChat: () => void;
}

export interface UseNewsReturn {
  news: NewsItem[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseLocalStorageReturn<T> {
  value: T;
  setValue: (value: T | ((prevValue: T) => T)) => void;
  removeValue: () => void;
}
