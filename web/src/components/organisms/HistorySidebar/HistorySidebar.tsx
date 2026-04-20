import React, { useState } from 'react';
import styles from './HistorySidebar.module.css';

export interface ChatSession {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messages: Array<{ role: string; content: string }>;
}

export interface HistorySidebarProps {
  activeChat?: string;
  onChatSelect?: (chatId: string) => void;
  onNewChat?: () => void;
}

const generateId = (): string => Math.random().toString(36).substring(2, 11);

export const HistorySidebar: React.FC<HistorySidebarProps> = ({
  activeChat,
  onChatSelect,
  onNewChat,
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(true);
  const [isMobileOpen, setIsMobileOpen] = useState<boolean>(false);
  
  const generateMockChats = (): ChatSession[] => [
    {
      id: generateId(),
      title: 'Consulta sobre becas',
      createdAt: new Date(Date.now() - 1000 * 60 * 30),
      updatedAt: new Date(Date.now() - 1000 * 60 * 30),
      messages: [
        { role: 'user', content: '¿Qué becas hay disponibles?' },
        { role: 'bot', content: 'La universidad ofrece varias opciones...' },
      ],
    },
    {
      id: generateId(),
      title: 'Información académica',
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24),
      updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 24),
      messages: [
        { role: 'user', content: '¿Cuáles son los requisitos?' },
        { role: 'bot', content: 'Los requisitos incluyen...' },
      ],
    },
  ];

  const [chats, setChats] = useState<ChatSession[]>(generateMockChats);

  const handleNewChat = (): void => {
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

  const handleSelectChat = (chatId: string): void => {
    if (onChatSelect) {
      onChatSelect(chatId);
    }
    setIsMobileOpen(false);
  };

  const formatDate = (date: Date): string => {
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

    const monthNames = [
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

    if (date.getFullYear() === today.getFullYear()) {
      return `${date.getDate()} ${monthNames[date.getMonth()]}`;
    }

    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
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
        className={`${styles.historySidebar} ${isOpen ? styles.open : styles.collapsed} ${
          isMobileOpen ? styles['mobile-open'] : ''
        }`}
      >
        <div className={styles.sidebarContent}>
          {/* Header */}
          <div className={styles.sidebarHeader}>
            <div className={styles.sidebarToggleWrapper}>
              <button
                className={styles.sidebarToggle}
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
              <button className={styles.newChatBtn} onClick={handleNewChat}>
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
            <div className={styles.chatHistory}>
              {sortedDateKeys.map((dateKey) => (
                <div key={dateKey} className={styles.chatGroup}>
                  <div className={styles.chatGroupLabel}>{dateKey}</div>
                  <div className={styles.chatItems}>
                    {groupedChats[dateKey].map((chat) => (
                      <button
                        key={chat.id}
                        className={`${styles.chatItem} ${
                          activeChat === chat.id ? styles.active : ''
                        }`}
                        onClick={() => handleSelectChat(chat.id)}
                        title={chat.title}
                      >
                        <div className={styles.chatItemContent}>
                          <span className={styles.chatTitle}>{chat.title}</span>
                        </div>
                        <div className={styles.chatItemActions}>
                          <button
                            className={styles.chatActionBtn}
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
          <div className={styles.sidebarFooter}>
            <button className={styles.sidebarFooterBtn} title="Configuración">
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
            <button className={styles.sidebarFooterBtn} title="Perfil">
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
};

export default HistorySidebar;
