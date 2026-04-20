import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import type { Message } from '../types/api.types';
import { ChatHeader } from '../components/organisms/ChatLayout/ChatHeader';
import { MessageInput } from '../components/molecules/MessageInput/MessageInput';
import { MessageBubble as MessageBubbleComponent } from '../components/molecules/MessageBubble/MessageBubble';
import { NewsSidebar } from '../components/organisms/NewsSidebar/NewsSidebar';
import { HistorySidebar } from '../components/organisms/HistorySidebar/HistorySidebar';
import NewsCarousel from '../components/molecules/NewsCarousel/NewsCarousel';
import TypingIndicator from '../components/molecules/TypingIndicator/TypingIndicator';
import styles from './ChatPage.module.css';

export const ChatPage: React.FC = () => {
  const { messages, isLoading, isOnline, sendMessage, clearChat } = useChat();
  
  const messagesEndRef: React.MutableRefObject<HTMLDivElement | null> = useRef(null);
  const [activeChat, setActiveChat] = useState<string | undefined>(undefined);
  const inputRef: React.MutableRefObject<HTMLTextAreaElement | null> = useRef(null);
  const [inputValue, setInputValue] = useState<string>('');

  const handleNewChat: () => void = useCallback(() => {
    clearChat();
    setInputValue('');
  }, [clearChat]);

  const scrollToBottom: () => void = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  return (
    <div className={styles.chatLayout}>
      <HistorySidebar
        activeChat={activeChat}
        onChatSelect={(chatId: string) => setActiveChat(chatId)}
        onNewChat={handleNewChat}
      />

      <main className={styles.chatPage}>
        <ChatHeader
          title="Botcachino"
          status={isLoading ? 'typing' : isOnline ? 'online' : 'offline'}
          onClear={clearChat}
        />

        <NewsCarousel />

        <div 
          className={styles.chatMessages}
          id="chat-messages"
          role="log"
          aria-live="polite"
        >
          <div className={styles.chatMessagesInner}>
            {messages.map((msg: Message) => (
              <MessageBubbleComponent key={msg.id} message={msg} />
            ))}
            
            {isLoading && <TypingIndicator />}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        <MessageInput
          onSend={sendMessage}
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
