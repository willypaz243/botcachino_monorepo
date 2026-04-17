import React from 'react';
import type { ChatHeaderProps } from '../../../types/component.types';
import styles from './ChatHeader.module.css';

export const ChatHeader: React.FC<ChatHeaderProps> = ({ 
  title,
  status,
  onClear,
}) => {
  const getStatusIndicator: () => React.ReactNode = () => {
    switch (status) {
      case 'typing':
        return <span className={styles.statusTextTyping}>Escribiendo...</span>;
      
      case 'online':
        return (
          <>
            <span className={styles.statusDot} />
            En línea
          </>
        );
      
      case 'offline':
        return (
          <>
            <span className={`${styles.statusDot} ${styles['statusDot--offline']}`} />
            Desconectado
          </>
        );
      
      default:
        return null;
    }
  };

  return (
    <header className={styles.chatHeader}>
      <div className={styles.chatHeaderLeft}>
        <div className={styles.chatHeaderLogo} aria-hidden="true">
          ☕️
        </div>
        
        <div className={styles.chatHeaderInfo}>
          <h1 className={styles.chatHeaderTitle}>{title}</h1>
          
          <span className={styles.chatHeaderStatus}>
            {getStatusIndicator()}
          </span>
        </div>
      </div>
      
      {onClear && (
        <button
          className={styles.chatHeaderClear}
          onClick={onClear}
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
      )}
    </header>
  );
};

export default ChatHeader;
