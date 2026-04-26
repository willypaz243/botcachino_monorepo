import React, { useState, useCallback, useEffect, useRef } from 'react';
import type { Message, SSEEvent, UseChatReturn } from '../types/hooks.types';
import { streamSSE }  from '../lib/sse';

const API_URL: string = import.meta.env.VITE_API_URL || '/api';
const STORAGE_KEY: string = 'botcachino_thread_id';

const INITIAL_MESSAGE: Message = {
  id: crypto.randomUUID(),
  role: 'bot',
  content: 
    '**¡Hola!** Soy Botcachino, tu asistente de la UMSS. ¿En qué puedo ayudarte hoy?',
  timestamp: new Date(),
  done: true,
};

function getOrCreateThreadId(): string {
  const stored: string | null = localStorage.getItem(STORAGE_KEY);
  
  if (stored !== null) {
    return stored;
  }
  
  const newId: string = crypto.randomUUID();
  localStorage.setItem(STORAGE_KEY, newId);
  return newId;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>(() => [INITIAL_MESSAGE]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOnline] = useState<boolean>(true);

  const threadIdRef: React.MutableRefObject<string> = useRef<string>(getOrCreateThreadId());
  const cancelRef: React.MutableRefObject<(() => void) | null> = useRef(null);
  const lastInfoIdRef: React.MutableRefObject<string | null> = useRef(null);
  const onDoneRef: React.MutableRefObject<((botMessageId: string) => void) | null> = useRef(null);

  useEffect(() => {
    const storedId: string | null = localStorage.getItem(STORAGE_KEY);
    
    if (storedId !== null) {
      threadIdRef.current = storedId;
    } else {
      const newId: string = crypto.randomUUID();
      localStorage.setItem(STORAGE_KEY, newId);
      threadIdRef.current = newId;
    }
  }, []);

  const sendMessage: (content: string, onBeforeSend?: () => Promise<void>) => void = useCallback(
    async (content: string, onBeforeSend?: () => Promise<void>) => {
      if (!content.trim() || isLoading) {
        return;
      }

      if (onBeforeSend !== null && onBeforeSend !== undefined) {
        await onBeforeSend();
      }

      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content: content,
        timestamp: new Date(),
        done: true,
      };

      const botMessageId: string = crypto.randomUUID();
      const botMessage: Message = {
        id: botMessageId,
        role: 'bot',
        content: '',
        timestamp: new Date(),
        done: false,
      };

      setMessages((prev: Message[]) => [...prev, userMessage, botMessage]);
      setIsLoading(true);

      cancelRef.current = streamSSE(
        `${API_URL}/agent/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: content,
            thread_id: threadIdRef.current,
          }),
        },
      (event: SSEEvent) => {
        if (event.type === 'text') {
          setMessages((prev: Message[]) => {
            const newMsgs: Message[] = [];
            
            for (const msg of prev) {
              if (msg.id === botMessageId) {
                newMsgs.push({
                  ...msg,
                  content: msg.content + event.content,
                });
              } else if (msg.id !== lastInfoIdRef.current) {
                newMsgs.push(msg);
              }
            }
            
            return newMsgs;
          });
        } else if (event.type === 'info') {
          const infoId: string = lastInfoIdRef.current || crypto.randomUUID();
          lastInfoIdRef.current = infoId;
          
          const infoMsg: Message = {
            id: infoId,
            role: 'info',
            content: event.content,
            timestamp: new Date(),
            done: true,
          };
          
          setMessages((prev: Message[]) => {
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
          setMessages((prev: Message[]) => {
            const newMsgs: Message[] = [];
            
            for (const msg of prev) {
              if (msg.id === botMessageId) {
                newMsgs.push({
                  ...msg,
                  content: `${msg.content}\n\n*${event.content}*`,
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
        const prevInfoId: string | null = lastInfoIdRef.current;
        lastInfoIdRef.current = null;
        
        setMessages((prev: Message[]) => {
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
        
        if (onDoneRef.current !== null) {
          onDoneRef.current(botMessageId);
        }
      },
      (error: Error) => {
        const prevInfoId: string | null = lastInfoIdRef.current;
        lastInfoIdRef.current = null;
        
        setMessages((prev: Message[]) => {
          const newMsgs: Message[] = [];
          
          for (const msg of prev) {
            if (msg.id === botMessageId) {
              newMsgs.push({
                ...msg,
                content: `${msg.content}\n\n*Error: ${error.message}*`,
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

  const clearChat: () => void = useCallback(() => {
    if (cancelRef.current !== null) {
      cancelRef.current();
      cancelRef.current = null;
    }

    const newId: string = crypto.randomUUID();
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
      if (cancelRef.current !== null) {
        cancelRef.current();
      }
    };
  }, []);

  const setThreadId: (threadId: string) => void = useCallback((threadId: string) => {
    localStorage.setItem(STORAGE_KEY, threadId);
    threadIdRef.current = threadId;
  }, []);

  const setOnDone: (cb: ((botMessageId: string) => void) | null) => void = useCallback((cb: ((botMessageId: string) => void) | null) => {
    onDoneRef.current = cb;
  }, []);

  return { messages, isLoading, isOnline, sendMessage, clearChat, setThreadId, setMessages, setOnDone };
}

export default useChat;
