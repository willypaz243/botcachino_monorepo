import React from 'react';
import type { ChatHeaderProps } from '../../../types/component.types';
import styles from './ChatHeader.module.css';

export const ChatHeader: React.FC<ChatHeaderProps> = ({ 
  title,
  status,
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
    </header>
  );
};

export default ChatHeader;
