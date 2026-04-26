import { useState, useCallback } from 'react';
import type { ConversationRead, MessageRead } from '../types/api.types';

const API_URL: string = import.meta.env.VITE_API_URL || '/api';

export interface UseHistoryReturn {
  conversations: ConversationRead[];
  isLoadingConversations: boolean;
  loadConversations: () => Promise<void>;
  loadMessages: (conversationUuid: string) => Promise<MessageRead[]>;
  createConversation: (title?: string) => Promise<ConversationRead>;
  saveMessage: (conversationUuid: string, role: 'user' | 'bot', content: string) => Promise<void>;
}

export function useHistory(): UseHistoryReturn {
  const [conversations, setConversations] = useState<ConversationRead[]>([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState<boolean>(false);

  const loadConversations: () => Promise<void> = useCallback(async () => {
    setIsLoadingConversations(true);
    try {
      const response: Response = await fetch(`${API_URL}/history/conversations/`);

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data: ConversationRead[] = await response.json();
      setConversations(data);
    } catch (err) {
      console.error('Failed to load conversations:', err);
      setConversations([]);
    } finally {
      setIsLoadingConversations(false);
    }
  }, []);

  const loadMessages: (conversationUuid: string) => Promise<MessageRead[]> = useCallback(
    async (conversationUuid: string) => {
      try {
        const response: Response = await fetch(
          `${API_URL}/history/conversations/${conversationUuid}/messages/`,
        );

        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }

        const data: MessageRead[] = await response.json();
        return data;
      } catch (err) {
        console.error('Failed to load messages:', err);
        return [];
      }
    },
    [],
  );

  const createConversation: (title?: string) => Promise<ConversationRead> = useCallback(async (title?: string) => {
    const conversationTitle = title || 'Nuevo chat';
    try {
      const response: Response = await fetch(`${API_URL}/history/conversations/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: conversationTitle }),
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data: ConversationRead = await response.json();
      setConversations((prev) => [data, ...prev]);
      return data;
    } catch (err) {
      console.error('Failed to create conversation:', err);
      throw err;
    }
  }, []);

  const saveMessage: (conversationUuid: string, role: 'user' | 'bot', content: string) => Promise<void> = useCallback(
    async (conversationUuid: string, role: 'user' | 'bot', content: string) => {
      try {
        const response: Response = await fetch(
          `${API_URL}/history/conversations/${conversationUuid}/messages/`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role, content }),
          },
        );

        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }
      } catch (err) {
        console.error('Failed to save message:', err);
      }
    },
    [],
  );

  return {
    conversations,
    isLoadingConversations,
    loadConversations,
    loadMessages,
    createConversation,
    saveMessage,
  };
}

export default useHistory;
