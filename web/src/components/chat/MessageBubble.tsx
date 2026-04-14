import './MessageBubble.css';

export interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

interface MessageBubbleProps {
  message: Message;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' });
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`message-row message-row--${isUser ? 'user' : 'bot'}`}>
      {!isUser && <div className="message-avatar">☕️</div>}
      <div className={`message-bubble message-bubble--${isUser ? 'user' : 'bot'}`}>
        <p className="message-text" dangerouslySetInnerHTML={{ __html: message.content }} />
        <span className="message-time">{formatTime(message.timestamp)}</span>
      </div>
      {isUser && <div className="message-avatar">👤</div>}
    </div>
  );
}