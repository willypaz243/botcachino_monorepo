import './HistorySidebar.css';

function formatDate(dateString) {
  const date = new Date(dateString);

  return new Intl.DateTimeFormat('es-BO', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

function getPreview(messages) {
  const lastUserMessage = [...messages].reverse().find((msg) => msg.role === 'user');
  if (!lastUserMessage) return 'Sin mensajes enviados';

  const text = lastUserMessage.content.replace(/\s+/g, ' ').trim();
  if (text.length <= 58) return text;
  return `${text.slice(0, 58)}...`;
}

export default function HistorySidebar({
  chats,
  activeChatId,
  onSelectChat,
  onNewChat,
  isOpen,
  onClose,
}) {
  const sortedChats = [...chats].sort(
    (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
  );

  return (
    <aside className={`history-sidebar ${isOpen ? 'history-sidebar--open' : ''}`}>
      <div className="history-sidebar-header">
        <h2 className="history-sidebar-title">Historial</h2>
        <button
          className="history-sidebar-new"
          onClick={onNewChat}
          type="button"
          aria-label="Crear nuevo chat"
        >
          + Nuevo chat
        </button>
      </div>

      <div className="history-sidebar-list" role="listbox" aria-label="Conversaciones anteriores">
        {sortedChats.map((chat) => {
          const isActive = chat.id === activeChatId;
          return (
            <button
              key={chat.id}
              className={`history-item ${isActive ? 'history-item--active' : ''}`}
              onClick={() => {
                onSelectChat(chat.id);
                onClose();
              }}
              type="button"
              role="option"
              aria-selected={isActive}
            >
              <span className="history-item-title">{chat.title}</span>
              <span className="history-item-preview">{getPreview(chat.messages)}</span>
              <span className="history-item-date">{formatDate(chat.updatedAt)}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}
