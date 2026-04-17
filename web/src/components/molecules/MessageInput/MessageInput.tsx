import React, { useRef, useEffect, type FormEvent, type KeyboardEvent } from 'react';
import styles from './MessageInput.module.css';

interface MessageInputProps {
  onSend: (_message: string) => void;
  disabled: boolean;
  value: string;
  onChange: (_value: string) => void;
  inputRef?: React.RefObject<HTMLTextAreaElement | null>;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSend,
  disabled,
  value,
  onChange,
  inputRef,
}) => {
  const textareaRef: React.MutableRefObject<HTMLTextAreaElement | null> = useRef(null);

  useEffect(() => {
    const el: HTMLTextAreaElement | null = textareaRef.current;
    
    if (el !== null) {
      el.style.height = 'auto';
      el.style.height = Math.min(el.scrollHeight, 160) + 'px';
    }
  }, [value]);

  function handleSubmit(e: FormEvent): void {
    e.preventDefault();
    
    if (!value.trim() || disabled) {
      return;
    }
    
    onSend(value);
    onChange('');
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>): void {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form className={styles.messageInputForm} onSubmit={handleSubmit}>
      <div className={styles.messageInputContainer}>
        <textarea
          ref={(el) => {
            textareaRef.current = el;
            if (inputRef !== undefined && inputRef !== null) {
              inputRef.current = el;
            }
          }}
          id="chat-input"
          className={styles.messageInputTextarea}
          placeholder="Escribe tu mensaje..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
          aria-label="Mensaje de chat"
        />
        
        <button
          type="submit"
          className={`${styles.messageInputSend} ${disabled || !value.trim() ? styles.messageInputSendDisabled : ''}`}
          disabled={disabled || !value.trim()}
          aria-label="Enviar mensaje"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
      
      <p className={styles.messageInputHint}>
        <kbd>Enter</kbd> para enviar · <kbd>Shift + Enter</kbd> nueva línea
      </p>
    </form>
  );
};

export default MessageInput;
