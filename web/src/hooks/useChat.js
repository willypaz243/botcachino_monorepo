import { useState, useCallback, useRef, useEffect } from 'react';

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'bot',
  content:
    '¡Hola! Soy **Botcachino**, tu asistente de noticias e información. Pregúntame lo que quieras sobre nuestro contenido.',
  timestamp: new Date().toISOString(),
};

let messageIdCounter = 0;

function createMessage(role, content) {
  return {
    id: `msg-${Date.now()}-${++messageIdCounter}`,
    role,
    content,
    timestamp: new Date().toISOString(),
  };
}

export function useChat() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  useEffect(() => {
    fetch('/api/chat')
      .then((res) => {
        const contentType = res.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          setIsOnline(true);
        } else {
          setIsOnline(false);
        }
      })
      .catch(() => setIsOnline(false));
  }, []);

  const sendMessage = useCallback(async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    setError(null);

    const userMsg = createMessage('user', trimmed);
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: trimmed }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      const botMsg = createMessage('bot', data.reply);
      setMessages((prev) => [...prev, botMsg]);
      setIsOnline(true);
    } catch (err) {
      if (err.name === 'AbortError') return;
      setIsOnline(false);
      const errorMsg = createMessage(
        'bot',
        'No pude conectarme al servidor.',
      );
      setMessages((prev) => [...prev, errorMsg]);
      setError(err.message);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [isLoading]);

  const clearChat = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    setError(null);
  }, []);

  return { messages, isLoading, isOnline, error, sendMessage, clearChat };
}
