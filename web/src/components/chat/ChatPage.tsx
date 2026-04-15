import { useState, useEffect, useRef } from "react";
import { useChat } from "../../hooks/useChat";
import MessageBubble from "./MessageBubble";
import MessageInput from "./MessageInput";
import TypingIndicator from "./TypingIndicator";
import NewsSidebar from "../news/NewsSidebar";
import { HistorySidebar } from "./Historial";
import "./ChatPage.css";

export default function ChatPage() {
  const { messages, isLoading, isOnline, sendMessage, clearChat } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [inputValue, setInputValue] = useState("");
  const [activeChat, setActiveChat] = useState<string>();

  const handleNewChat = () => {
    clearChat();
    setInputValue("");
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="chat-layout">
      <HistorySidebar
        activeChat={activeChat}
        onChatSelect={(chatId) => setActiveChat(chatId)}
        onNewChat={handleNewChat}
      />

      <div className="chat-page">
        <header className="chat-header">
          <div className="chat-header-left">
            <div className="chat-header-logo" aria-hidden="true">
              ☕️
            </div>
            <div className="chat-header-info">
              <h1 className="chat-header-title">Botcachino</h1>
              <span className="chat-header-status">
                {isLoading ? (
                  <span className="status-typing-text">Escribiendo...</span>
                ) : isOnline ? (
                  <>
                    <span className="status-dot" />
                    En línea
                  </>
                ) : (
                  <>
                    <span className="status-dot status-dot--offline" />
                    Desconectado
                  </>
                )}
              </span>
            </div>
          </div>
          <button
            className="chat-header-clear"
            onClick={clearChat}
            title="Limpiar conversación"
            aria-label="Limpiar conversación"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        </header>

        <main
          className="chat-messages"
          id="chat-messages"
          role="log"
          aria-live="polite"
        >
          <div className="chat-messages-inner">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        </main>

        <MessageInput
          onSend={sendMessage}
          disabled={isLoading}
          value={inputValue}
          onChange={setInputValue}
        />
      </div>

      <NewsSidebar onSelect={(texto) => setInputValue(texto)} />
    </div>
  );
}