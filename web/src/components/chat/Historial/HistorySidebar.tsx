import { useState } from 'react';
import { ChatSession, HistorySidebarProps } from './types';
import { MOCK_CHATS } from './mockChats';
import './HistorySidebar.css';

const generateId = (): string => Math.random().toString(36).substring(2, 11);

export function HistorySidebar({
  activeChat,
  onChatSelect,
  onNewChat,
}: HistorySidebarProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [chats, setChats] = useState<ChatSession[]>(MOCK_CHATS);

  const handleNewChat = () => {
    const newChat: ChatSession = {
      id: generateId(),
      title: 'Nuevo chat',
      createdAt: new Date(),
      updatedAt: new Date(),
      messages: [],
    };

    setChats([newChat, ...chats]);

    if (onNewChat) {
      onNewChat();
    }

    if (onChatSelect) {
      onChatSelect(newChat.id);
    }
  };

  const handleSelectChat = (chatId: string) => {
    if (onChatSelect) {
      onChatSelect(chatId);
    }
  };

  const formatDate = (date: Date) => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (
      date.getFullYear() === today.getFullYear() &&
      date.getMonth() === today.getMonth() &&
      date.getDate() === today.getDate()
    ) {
      return 'Hoy';
    }

    if (
      date.getFullYear() === yesterday.getFullYear() &&
      date.getMonth() === yesterday.getMonth() &&
      date.getDate() === yesterday.getDate()
    ) {
      return 'Ayer';
    }

    const daysAgo = Math.floor(
      (today.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysAgo < 7) {
      return `Hace ${daysAgo}d`;
    }

    if (
      date.getFullYear() === today.getFullYear() &&
      date.getMonth() === today.getMonth()
    ) {
      return `${date.getDate()} ${getMonthName(date.getMonth())}`;
    }

    return `${date.getDate()}/
${date.getMonth() + 1}/${date.getFullYear()}`;
  };

  const getMonthName = (month: number) => {
    const months = [
      'Ene',
      'Feb',
      'Mar',
      'Abr',
      'May',
      'Jun',
      'Jul',
      'Ago',
      'Sep',
      'Oct',
      'Nov',
      'Dic',
    ];
    return months[month];
  };

  const groupedChats = chats.reduce(
    (acc, chat) => {
      const dateKey = formatDate(chat.createdAt);
      if (!acc[dateKey]) {
        acc[dateKey] = [];
      }
      acc[dateKey].push(chat);
      return acc;
    },
    {} as Record<string, ChatSession[]>
  );

  const dateOrder = ['Hoy', 'Ayer'];
  const sortedDateKeys = Object.keys(groupedChats).sort((a, b) => {
    const aIndex = dateOrder.indexOf(a);
    const bIndex = dateOrder.indexOf(b);
    if (aIndex !== -1 && bIndex !== -1) return aIndex - bIndex;
    if (aIndex !== -1) return -1;
    if (bIndex !== -1) return 1;
    return 0;
  });

  return (
    <>
    

      <aside
        className={`history-sidebar ${isOpen ? 'open' : 'collapsed'} ${
          isMobileOpen ? 'mobile-open' : ''
        }`}
      >
        {/* Sidebar Content */}
        <div className="sidebar-content">
          {/* Header */}
          <div className="sidebar-header">
            <div className="sidebar-toggle-wrapper">
              <button
                className="sidebar-toggle"
                onClick={() => setIsOpen(!isOpen)}
                title={isOpen ? 'Contraer' : 'Expandir'}
                aria-label="Toggle sidebar"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <line x1="3" y1="6" x2="21" y2="6" />
                  <line x1="3" y1="12" x2="21" y2="12" />
                  <line x1="3" y1="18" x2="21" y2="18" />
                </svg>
              </button>
            </div>

            {isOpen && (
              <button className="new-chat-btn" onClick={handleNewChat}>
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M12 5v14M5 12h14" />
                </svg>
                <span>Nuevo chat</span>
              </button>
            )}
          </div>

          {/* Chat History */}
          {isOpen && (
            <div className="chat-history">
              {sortedDateKeys.map((dateKey) => (
                <div key={dateKey} className="chat-group">
                  <div className="chat-group-label">{dateKey}</div>
                  <div className="chat-items">
                    {groupedChats[dateKey].map((chat) => (
                      <button
                        key={chat.id}
                        className={`chat-item ${
                          activeChat === chat.id ? 'active' : ''
                        }`}
                        onClick={() => {
                          handleSelectChat(chat.id);
                          setIsMobileOpen(false);
                        }}
                        title={chat.title}
                      >
                        <div className="chat-item-content">
                          <span className="chat-title">{chat.title}</span>
                        </div>
                        <div className="chat-item-actions">
                          <button
                            className="chat-action-btn"
                            onClick={(e) => {
                              e.stopPropagation();
                            }}
                            title="Opciones"
                          >
                            <svg
                              width="16"
                              height="16"
                              viewBox="0 0 24 24"
                              fill="currentColor"
                            >
                              <circle cx="12" cy="5" r="2" />
                              <circle cx="12" cy="12" r="2" />
                              <circle cx="12" cy="19" r="2" />
                            </svg>
                          </button>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar Footer */}
        {isOpen && (
          <div className="sidebar-footer">
            <button className="sidebar-footer-btn" title="Configuración">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <circle cx="12" cy="12" r="3" />
                <path d="M12 1v6m0 6v6M4.22 4.22l4.24 4.24m5.08 5.08l4.24 4.24M1 12h6m6 0h6M4.22 19.78l4.24-4.24m5.08-5.08l4.24-4.24" />
              </svg>
            </button>
            <button className="sidebar-footer-btn" title="Perfil">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
