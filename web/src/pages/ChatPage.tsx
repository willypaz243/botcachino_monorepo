import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import { useHistory } from '../hooks/useHistory';
import type { MessageRead } from '../types/api.types';
import { ChatHeader } from '../components/organisms/ChatLayout/ChatHeader';
import { MessageInput } from '../components/molecules/MessageInput/MessageInput';
import { MessageBubble as MessageBubbleComponent } from '../components/molecules/MessageBubble/MessageBubble';
import { NewsSidebar } from '../components/organisms/NewsSidebar/NewsSidebar';
import { HistorySidebar } from '../components/organisms/HistorySidebar/HistorySidebar';
import NewsCarousel from '../components/molecules/NewsCarousel/NewsCarousel';
import TypingIndicator from '../components/molecules/TypingIndicator/TypingIndicator';
import styles from './ChatPage.module.css';

const STORAGE_KEY: string = 'botcachino_thread_id';

export const ChatPage: React.FC = () => {
  const { messages, isLoading, isOnline, sendMessage, clearChat, setThreadId, setMessages, setOnDone } = useChat();
  const { loadMessages, loadConversations, createConversation, conversations, isLoadingConversations } = useHistory();
  
  const messagesEndRef: React.MutableRefObject<HTMLDivElement | null> = useRef(null);
  const [activeChat, setActiveChat] = useState<string | undefined>(undefined);
  const inputRef: React.MutableRefObject<HTMLTextAreaElement | null> = useRef(null);
  const [inputValue, setInputValue] = useState<string>('');
  const loadConversationsRef = useRef(loadConversations);

  useEffect(() => {
    loadConversationsRef.current = loadConversations;
  }, [loadConversations]);

  const scrollToBottom: () => void = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleCreateChat: () => void = useCallback(() => {
    clearChat();
    setInputValue('');
    setActiveChat(undefined);
    localStorage.setItem(STORAGE_KEY, crypto.randomUUID());
  }, [clearChat]);

  const persistMessages: (botMessageId: string) => Promise<void> = useCallback(async (_botMessageId: string) => {
    // Backend already saves messages in _save_conversation
    // Just refetch conversations to update sidebar
    
    try {
      await new Promise((resolve) => setTimeout(resolve, 300));
      await loadConversationsRef.current();
    } catch (err) {
      console.error('Failed to refetch conversations:', err);
    }
  }, []);

  const handleSendMessage: (content: string) => Promise<void> = useCallback(
    async (content: string) => {
      // On FIRST user message, always create a new conversation in DB
      if (messages.length === 1) {
        const title = content.trim().split(/\s+/).slice(0, 5).join(' ') || 'Nuevo chat';
        
        try {
          const newConv = await createConversation(title);
          const newUuid = newConv.uuid;
          
          // Update storage FIRST, then wait for setThreadId to complete
          localStorage.setItem(STORAGE_KEY, newUuid);
          setThreadId(newUuid);
          setActiveChat(newUuid);
          
          // Wait a tick to ensure threadId is updated before sending
          await new Promise((resolve) => setTimeout(resolve, 0));
        } catch (err) {
          console.error('Failed to create conversation:', err);
        }
      }

      setOnDone(persistMessages);
      sendMessage(content);
    },
    [messages.length, createConversation, sendMessage, setOnDone, persistMessages, setThreadId],
  );

  const handleSelectChat: (chatId: string) => Promise<void> = useCallback(async (chatId: string) => {
    setActiveChat(chatId);
    
    try {
      const threadId: string = chatId;
      localStorage.setItem(STORAGE_KEY, threadId);
      setThreadId(threadId);
      
      const messagesData: MessageRead[] = await loadMessages(chatId);
      
      if (messagesData.length === 0) {
        const initialMsg = {
          id: crypto.randomUUID(),
          role: 'bot' as const,
          content: '**¡Hola!** Soy Botcachino, tu asistente de la UMSS. ¿En qué puedo ayudarte hoy?',
          timestamp: new Date(),
          done: true,
        };
        setMessages([initialMsg]);
      } else {
        const convertedMessages = messagesData.map((msg: MessageRead) => ({
          id: msg.uuid,
          role: (msg.role === 'bot' ? 'assistant' : 'user') as 'user' | 'bot',
          content: msg.content,
          timestamp: new Date(msg.timestamp),
          done: true,
        }));
        setMessages(convertedMessages);
      }
      
      await loadConversations();
    } catch (err) {
      console.error('Failed to load conversation:', err);
    }
  }, [loadMessages, loadConversations, setThreadId, setMessages]);

  return (
    <div className={styles.chatLayout}>
      <HistorySidebar
        activeChat={activeChat}
        conversations={conversations}
        isLoadingConversations={isLoadingConversations}
        onChatSelect={handleSelectChat}
        onCreateChat={handleCreateChat}
        onRefetchConversations={loadConversations}
      />

      <main className={styles.chatPage}>
        <ChatHeader
          title="Botcachino"
          status={isLoading ? 'typing' : isOnline ? 'online' : 'offline'}
        />

        <NewsCarousel />

        <div 
          className={styles.chatMessages}
          id="chat-messages"
          role="log"
          aria-live="polite"
        >
          <div className={styles.chatMessagesInner}>
            {messages.map((msg) => (
              <MessageBubbleComponent key={msg.id} message={msg} />
            ))}
            
            {isLoading && <TypingIndicator />}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        <MessageInput
          onSend={handleSendMessage}
          disabled={isLoading}
          value={inputValue}
          onChange={setInputValue}
          inputRef={inputRef}
        />
      </main>

      <NewsSidebar onSelect={(texto: string) => {
        setInputValue(texto);
        inputRef.current?.focus();
      }} />
    </div>
  );
};

export default ChatPage;
