import { useRef, useEffect, type FormEvent, type KeyboardEvent } from 'react';
import './MessageInput.css';

interface MessageInputProps {
  onSend: (_message: string) => void;
  disabled: boolean;
  value: string;
  onChange: (_value: string) => void;
}

export default function MessageInput({ onSend, disabled, value, onChange }: MessageInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = Math.min(el.scrollHeight, 160) + 'px';
    }
  }, [value]);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value);
    onChange('');
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <div className="message-input-container">
        <textarea
          ref={textareaRef}
          id="chat-input"
          className="message-input-textarea"
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
          className="message-input-send"
          disabled={disabled || !value.trim()}
          aria-label="Enviar mensaje"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
      <p className="message-input-hint">
        <kbd>Enter</kbd> para enviar · <kbd>Shift + Enter</kbd> nueva línea
      </p>
    </form>
  );
}