import './MessageBubble.css';
/**
 * Formats bold markdown (**text**) to <strong> tags.
 */
function formatContent(text) {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

function formatTime(isoString) {
  const date = new Date(isoString);
  return date.toLocaleTimeString('es-BO', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`message-row ${isUser ? 'message-row--user' : 'message-row--bot'}`}
    >
      {!isUser && (
        <div className="message-avatar" aria-hidden="true">
          ☕️
        </div>
      )}

      <div className={`message-bubble ${isUser ? 'message-bubble--user' : 'message-bubble--bot'}`}>
        <p className="message-text">{formatContent(message.content)}</p>
        <time className="message-time" dateTime={message.timestamp}>
          {formatTime(message.timestamp)}
        </time>
      </div>
    </div>
  );
}
