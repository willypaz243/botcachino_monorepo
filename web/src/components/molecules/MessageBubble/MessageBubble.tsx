import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import type { Message } from '../../../types/api.types';
import styles from './MessageBubble.module.css';

interface MessageBubbleProps {
  message: Message;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('es', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  message 
}) => {
  const isUser: boolean = message.role === 'user';
  const isInfo: boolean = message.role === 'info';

  if (isInfo) {
    return (
      <div className={`${styles.messageRow} ${styles['messageRow--info']}`}>
        <div className={styles.messageBubble}>
          <p className={`${styles.messageText} ${styles['messageText--info']}`}>
            {message.content}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.messageRow} ${isUser ? styles['messageRow--user'] : styles['messageRow--bot']}`}>
      {!isUser && <div className={styles.avatar} aria-hidden="true">☕️</div>}
      
      <div className={`${styles.messageBubble} ${isUser ? styles['messageBubble--user'] : styles['messageBubble--bot']}`}>
        {isUser ? (
          <p className={styles.messageText}>{message.content}</p>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              p: ({ children }) => (
                <p className={styles.messageText}>
                  {children}
                </p>
              ),
              table: ({ children }) => (
                <div className={styles.tableWrapper}>
                  <table className={styles.messageTable}>{children}</table>
                </div>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        
        <span className={styles.messageTime}>
          {formatTime(message.timestamp)}
        </span>
      </div>
      
      {isUser && <div className={styles.avatar} aria-hidden="true">👤</div>}
    </div>
  );
};

export default MessageBubble;
