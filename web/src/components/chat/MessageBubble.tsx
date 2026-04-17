import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import './MessageBubble.css';

export interface Message {
  id: string;
  role: 'user' | 'bot' | 'info';
  content: string;
  timestamp: Date;
  done?: boolean;
}

interface MessageBubbleProps {
  message: Message;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' });
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isInfo = message.role === 'info';

  if (isInfo) {
    return (
      <div className="message-row message-row--info">
        <div className="message-bubble message-bubble--info">
          <p className="message-text message-text--info">{message.content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`message-row message-row--${isUser ? 'user' : 'bot'}`}>
      {!isUser && <div className="message-avatar">☕️</div>}
      <div className={`message-bubble message-bubble--${isUser ? 'user' : 'bot'}`}>
        {isUser ? (
          <p className="message-text">{message.content}</p>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              p: ({ children }) => <p className="message-text">{children}</p>,
              table: ({ children }) => (
                <div className="table-wrapper">
                  <table className="message-table">{children}</table>
                </div>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        <span className="message-time">{formatTime(message.timestamp)}</span>
      </div>
      {isUser && <div className="message-avatar">👤</div>}
    </div>
  );
}