import { useState, useCallback, useEffect, useRef } from 'react';
import type { Message } from '../components/chat/MessageBubble';
import { streamSSE, type SSEEvent } from '../lib/sse';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const STORAGE_KEY = 'botcachino_thread_id';

const INITIAL_MESSAGE: Message = {
  id: crypto.randomUUID(),
  role: 'bot',
  content: '**¡Hola!** Soy Botcachino, tu asistente de la UMSS. ¿En qué puedo ayudarte hoy?',
  timestamp: new Date(),
  done: true,
};

function getOrCreateThreadId(): string {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    return stored;
  }
  const newId = crypto.randomUUID();
  localStorage.setItem(STORAGE_KEY, newId);
  return newId;
}



interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  isOnline: boolean;
  sendMessage: (content: string) => void;
  clearChat: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>(() => [INITIAL_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline] = useState(true);

  const threadIdRef = useRef<string>(getOrCreateThreadId());
  const cancelRef = useRef<(() => void) | null>(null);
  const lastInfoIdRef = useRef<string | null>(null);

  useEffect(() => {
    const storedId = localStorage.getItem(STORAGE_KEY);
    if (storedId) {
      threadIdRef.current = storedId;
    } else {
      const newId = crypto.randomUUID();
      localStorage.setItem(STORAGE_KEY, newId);
      threadIdRef.current = newId;
    }
  }, []);

  const sendMessage = useCallback((content: string) => {
    if (!content.trim() || isLoading) {
      return;
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: content,
      timestamp: new Date(),
      done: true,
    };

    const botMessageId = crypto.randomUUID();
    const botMessage: Message = {
      id: botMessageId,
      role: 'bot',
      content: '',
      timestamp: new Date(),
      done: false,
    };

    setMessages((prev) => [...prev, userMessage, botMessage]);
    setIsLoading(true);

    cancelRef.current = streamSSE(
      `${API_URL}/agent/chat`,
      {
        method: 'POST',
        body: JSON.stringify({
          message: content,
          thread_id: threadIdRef.current,
        }),
      },
      (event: SSEEvent) => {
        if (event.type === 'text') {
          setMessages((prev) => {
            const newMsgs: Message[] = [];
            for (const msg of prev) {
              if (msg.id === botMessageId) {
                newMsgs.push({ ...msg, content: msg.content + event.content });
              } else if (msg.id !== lastInfoIdRef.current) {
                newMsgs.push(msg);
              }
            }
            return newMsgs;
          });
        } else if (event.type === 'info') {
          const infoId = lastInfoIdRef.current || crypto.randomUUID();
          lastInfoIdRef.current = infoId;
          const infoMsg: Message = {
            id: infoId,
            role: 'info',
            content: event.content,
            timestamp: new Date(),
            done: true,
          };
          setMessages((prev) => {
            const newMsgs: Message[] = [];
            for (const msg of prev) {
              if (msg.id === botMessageId) {
                newMsgs.push(msg);
              } else if (msg.id !== lastInfoIdRef.current) {
                newMsgs.push(msg);
              }
            }
            return [...newMsgs, infoMsg];
          });
        } else if (event.type === 'error') {
          setMessages((prev) => {
            const newMsgs: Message[] = [];
            for (const msg of prev) {
              if (msg.id === botMessageId) {
                newMsgs.push({
                  ...msg,
                  content: msg.content + `\n\n*${event.content}*`,
                  done: true,
                });
              } else if (msg.id !== lastInfoIdRef.current) {
                newMsgs.push(msg);
              }
            }
            return newMsgs;
          });
        }
      },
      () => {
        const prevInfoId = lastInfoIdRef.current;
        lastInfoIdRef.current = null;
        setMessages((prev) => {
          const newMsgs: Message[] = [];
          for (const msg of prev) {
            if (msg.id === botMessageId) {
              newMsgs.push({ ...msg, done: true });
            } else if (msg.id !== prevInfoId) {
              newMsgs.push(msg);
            }
          }
          return newMsgs;
        });
        setIsLoading(false);
      },
      (error: Error) => {
        const prevInfoId = lastInfoIdRef.current;
        lastInfoIdRef.current = null;
        setMessages((prev) => {
          const newMsgs: Message[] = [];
          for (const msg of prev) {
            if (msg.id === botMessageId) {
              newMsgs.push({
                ...msg,
                content: msg.content + `\n\n*Error: ${error.message}*`,
                done: true,
              });
            } else if (msg.id !== prevInfoId) {
              newMsgs.push(msg);
            }
          }
          return newMsgs;
        });
        setIsLoading(false);
      },
    );
  }, [isLoading]);

  const clearChat = useCallback(() => {
    if (cancelRef.current) {
      cancelRef.current();
      cancelRef.current = null;
    }

    const newId = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, newId);
    threadIdRef.current = newId;

    const initialMessage: Message = {
      ...INITIAL_MESSAGE,
      id: crypto.randomUUID(),
      timestamp: new Date(),
    };

    setMessages([initialMessage]);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    return () => {
      if (cancelRef.current) {
        cancelRef.current();
      }
    };
  }, []);

  return { messages, isLoading, isOnline, sendMessage, clearChat };
}