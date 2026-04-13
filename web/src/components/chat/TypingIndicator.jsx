import './TypingIndicator.css';

export default function TypingIndicator() {
  return (
    <div className="typing-indicator" aria-label="El bot está escribiendo">
      <div className="typing-avatar">☕️</div>
      <div className="typing-dots">
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  );
}
