import { useState, useCallback, useRef, useEffect } from 'react';

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'bot',
  content:
    '¡Hola! Soy **Botcachino**, tu asistente de noticias e información. Pregúntame lo que quieras sobre nuestro contenido.',
  timestamp: new Date().toISOString(),
};

const CHAT_STORAGE_KEY = 'botcachino.chatHistory.v1';
const TITLE_MAX_LENGTH = 42;

let messageIdCounter = 0;

function createMessage(role, content) {
  return {
    id: `msg-${Date.now()}-${++messageIdCounter}`,
    role,
    content,
    timestamp: new Date().toISOString(),
  };
}

function createChat(title = 'Nuevo chat') {
  const now = new Date().toISOString();

  return {
    id: `chat-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    title,
    createdAt: now,
    updatedAt: now,
    messages: [WELCOME_MESSAGE],
  };
}

function generateTitleFromMessage(text) {
  const cleanText = text.replace(/\s+/g, ' ').trim();
  if (!cleanText) return 'Nuevo chat';
  if (cleanText.length <= TITLE_MAX_LENGTH) return cleanText;
  return `${cleanText.slice(0, TITLE_MAX_LENGTH)}...`;
}

function normalizeChat(rawChat) {
  if (!rawChat || !Array.isArray(rawChat.messages)) return null;

  const normalizedMessages = rawChat.messages
    .filter((msg) => msg && msg.id && msg.role && msg.content)
    .map((msg) => ({
      id: String(msg.id),
      role: msg.role,
      content: String(msg.content),
      timestamp: msg.timestamp || new Date().toISOString(),
    }));

  return {
    id: rawChat.id || `chat-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    title: rawChat.title || 'Nuevo chat',
    createdAt: rawChat.createdAt || new Date().toISOString(),
    updatedAt: rawChat.updatedAt || rawChat.createdAt || new Date().toISOString(),
    messages: normalizedMessages.length > 0 ? normalizedMessages : [WELCOME_MESSAGE],
  };
}

function loadStoredChats() {
  if (typeof window === 'undefined') {
    const defaultChat = createChat('Chat inicial');
    return {
      chats: [defaultChat],
      activeChatId: defaultChat.id,
    };
  }

  try {
    const raw = window.localStorage.getItem(CHAT_STORAGE_KEY);
    if (!raw) {
      const defaultChat = createChat('Chat inicial');
      return {
        chats: [defaultChat],
        activeChatId: defaultChat.id,
      };
    }

    const parsed = JSON.parse(raw);
    const parsedChats = Array.isArray(parsed?.chats)
      ? parsed.chats.map(normalizeChat).filter(Boolean)
      : [];

    if (parsedChats.length === 0) {
      const defaultChat = createChat('Chat inicial');
      return {
        chats: [defaultChat],
        activeChatId: defaultChat.id,
      };
    }

    const activeChatExists = parsedChats.some((chat) => chat.id === parsed?.activeChatId);

    return {
      chats: parsedChats,
      activeChatId: activeChatExists ? parsed.activeChatId : parsedChats[0].id,
    };
  } catch {
    const defaultChat = createChat('Chat inicial');
    return {
      chats: [defaultChat],
      activeChatId: defaultChat.id,
    };
  }
}

export function useChat() {
  const initialState = loadStoredChats();
  const [chats, setChats] = useState(initialState.chats);
  const [activeChatId, setActiveChatId] = useState(initialState.activeChatId);
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  const activeChat = chats.find((chat) => chat.id === activeChatId) || chats[0];
  const messages = activeChat?.messages || [WELCOME_MESSAGE];

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

  useEffect(() => {
    if (typeof window === 'undefined') return;

    window.localStorage.setItem(
      CHAT_STORAGE_KEY,
      JSON.stringify({ chats, activeChatId }),
    );
  }, [chats, activeChatId]);

  const sendMessage = useCallback(async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading || !activeChatId) return;

    setError(null);

    const userMsg = createMessage('user', trimmed);
    setChats((prevChats) => prevChats.map((chat) => {
      if (chat.id !== activeChatId) return chat;

      const shouldUpdateTitle = chat.messages.filter((msg) => msg.role === 'user').length === 0;
      const nextTitle = shouldUpdateTitle
        ? generateTitleFromMessage(trimmed)
        : chat.title;

      return {
        ...chat,
        title: nextTitle,
        updatedAt: new Date().toISOString(),
        messages: [...chat.messages, userMsg],
      };
    }));
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
      setChats((prevChats) => prevChats.map((chat) => {
        if (chat.id !== activeChatId) return chat;
        return {
          ...chat,
          updatedAt: new Date().toISOString(),
          messages: [...chat.messages, botMsg],
        };
      }));
      setIsOnline(true);
    } catch (err) {
      if (err.name === 'AbortError') return;
      setIsOnline(false);
      const errorMsg = createMessage(
        'bot',
        'No pude conectarme al servidor.',
      );
      setChats((prevChats) => prevChats.map((chat) => {
        if (chat.id !== activeChatId) return chat;
        return {
          ...chat,
          updatedAt: new Date().toISOString(),
          messages: [...chat.messages, errorMsg],
        };
      }));
      setError(err.message);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [activeChatId, isLoading]);

  const clearChat = useCallback(() => {
    if (!activeChatId) return;

    setChats((prevChats) => prevChats.map((chat) => {
      if (chat.id !== activeChatId) return chat;
      return {
        ...chat,
        title: 'Nuevo chat',
        updatedAt: new Date().toISOString(),
        messages: [WELCOME_MESSAGE],
      };
    }));
    setError(null);
  }, [activeChatId]);

  const createNewChat = useCallback(() => {
    const newChat = createChat();
    setChats((prevChats) => [newChat, ...prevChats]);
    setActiveChatId(newChat.id);
    setError(null);
  }, []);

  const selectChat = useCallback((chatId) => {
    setActiveChatId(chatId);
    setError(null);
  }, []);

  return {
    chats,
    activeChatId,
    messages,
    isLoading,
    isOnline,
    error,
    sendMessage,
    clearChat,
    createNewChat,
    selectChat,
  };
}
