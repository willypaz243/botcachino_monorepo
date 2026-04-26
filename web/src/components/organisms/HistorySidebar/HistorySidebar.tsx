import React, { useState } from 'react';
import type { ConversationRead } from '../../../types/api.types';
import styles from './HistorySidebar.module.css';

export interface HistorySidebarProps {
  activeChat?: string;
  conversations?: ConversationRead[];
  isLoadingConversations?: boolean;
  onChatSelect?: (chatId: string) => void;
  onCreateChat?: () => void;
  onRefetchConversations?: () => void;
}

export const HistorySidebar: React.FC<HistorySidebarProps> = ({
  activeChat,
  conversations = [],
  isLoadingConversations = false,
  onChatSelect,
  onCreateChat,
  onRefetchConversations,
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(true);
  const [isMobileOpen, setIsMobileOpen] = useState<boolean>(false);

  const handleNewChat: () => void = () => {
    if (onRefetchConversations) {
      onRefetchConversations();
    }
    if (onCreateChat) {
      onCreateChat();
    }
    if (onChatSelect) {
      onChatSelect(crypto.randomUUID());
    }
  };

  const handleSelectChat = (chatId: string): void => {
    if (onChatSelect) {
      onChatSelect(chatId);
    }
    setIsMobileOpen(false);
  };

  const formatDate = (dateStr: string): string => {
    const date: Date = new Date(dateStr);
    const today: Date = new Date();
    const yesterday: Date = new Date(today);
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

    const daysAgo: number = Math.floor(
      (today.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysAgo < 7) {
      return `Hace ${daysAgo}d`;
    }

    const monthNames: string[] = [
      'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic',
    ];

    if (date.getFullYear() === today.getFullYear()) {
      return `${date.getDate()} ${monthNames[date.getMonth()]}`;
    }

    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
  };

  const groupedChats: Record<string, ConversationRead[]> = conversations.reduce(
    (acc: Record<string, ConversationRead[]>, conv: ConversationRead) => {
      const dateKey: string = formatDate(conv.updated_at);
      if (!acc[dateKey]) {
        acc[dateKey] = [];
      }
      acc[dateKey].push(conv);
      return acc;
    },
    {} as Record<string, ConversationRead[]>
  );

  const dateOrder: string[] = ['Hoy', 'Ayer'];
  const sortedDateKeys: string[] = Object.keys(groupedChats).sort((a: string, b: string) => {
    const aIndex: number = dateOrder.indexOf(a);
    const bIndex: number = dateOrder.indexOf(b);
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
              {isLoadingConversations ? (
                <div className={styles.loadingText}>Cargando...</div>
              ) : sortedDateKeys.length === 0 ? (
                <div className={styles.emptyState}>No hay conversaciones</div>
              ) : (
                sortedDateKeys.map((dateKey: string) => (
                  <div key={dateKey} className={styles.chatGroup}>
                    <div className={styles.chatGroupLabel}>{dateKey}</div>
                    <div className={styles.chatItems}>
                      {groupedChats[dateKey].map((conv: ConversationRead) => (
                        <button
                          key={conv.uuid}
                          className={`${styles.chatItem} ${
                            activeChat === conv.uuid ? styles.active : ''
                          }`}
                          onClick={() => handleSelectChat(conv.uuid)}
                          title={conv.title}
                        >
                          <div className={styles.chatItemContent}>
                            <span className={styles.chatTitle}>{conv.title}</span>
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
                ))
              )}
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
