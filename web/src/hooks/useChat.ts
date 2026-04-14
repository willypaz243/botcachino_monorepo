import { useState, useCallback } from 'react';
import type { Message } from '../components/chat/MessageBubble';

interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  isOnline: boolean;
  sendMessage: (content: string) => void;
  clearChat: () => void;
}

const INITIAL_MESSAGE: Message = {
  id: crypto.randomUUID(),
  role: 'bot',
  content: '<strong>¡Hola!</strong> Soy Botcachino, tu asistente de la UMSS. ¿En qué puedo ayudarte hoy?',
  timestamp: new Date(),
};

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>(() => [INITIAL_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline] = useState(true);

  const sendMessage = useCallback((_content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: _content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    setTimeout(() => {
      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: 'bot',
        content: `<strong>Botcachino dice:</strong> Recibí tu mensaje: "${_content}". Esta es una respuesta simulada.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
      setIsLoading(false);
    }, 1500);
  }, []);

  const clearChat = useCallback(() => {
    setMessages([INITIAL_MESSAGE]);
  }, []);

  return { messages, isLoading, isOnline, sendMessage, clearChat };
}