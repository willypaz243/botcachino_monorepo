/**
 * Tipos TypeScript para el componente HistorySidebar
 */

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messages: Message[];
}

export interface HistorySidebarProps {
  activeChat?: string;
  onChatSelect?: (chatId: string) => void;
  onNewChat?: () => void;
}
