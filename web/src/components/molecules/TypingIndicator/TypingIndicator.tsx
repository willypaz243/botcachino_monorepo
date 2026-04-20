import React from 'react';
import styles from './TypingIndicator.module.css';

export const TypingIndicator: React.FC = () => {
  return (
    <div className={styles.typingIndicator} aria-label="El bot está escribiendo">
      <div className={styles.typingAvatar}>☕️</div>
      
      <div className={styles.typingDots}>
        <span className={styles.typingDot} />
        <span className={styles.typingDot} />
        <span className={styles.typingDot} />
      </div>
    </div>
  );
};

export default TypingIndicator;
