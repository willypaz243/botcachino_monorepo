import React, { useState } from 'react';
import { Newspaper, X } from 'lucide-react';
import styles from './NewsSidebar.module.css';

interface NewsItem {
  id: number;
  title: string;
  category: string;
  emoji: string;
}

interface NewsSidebarProps {
  onSelect: (texto: string) => void;
}

const MOCK_NEWS: NewsItem[] = [
  {
    id: 1,
    title: "¿Cuáles son los requisitos para inscribirse a Ingeniería de Sistemas?",
    category: "Inscripciones",
    emoji: "📚",
  },
  {
    id: 2,
    title: "¿Cuándo empieza el calendario académico 2025?",
    category: "Académico",
    emoji: "📅",
  },
  {
    id: 3,
    title: "¿Cómo obtengo mi certificado de notas en la UMSS?",
    category: "Trámites",
    emoji: "📄",
  },
  {
    id: 4,
    title: "¿Qué facultades ofrece la Universidad Mayor de San Simón?",
    category: "Facultades",
    emoji: "🏫️",
  },
  {
    id: 5,
    title: "¿Dónde queda el campus central de la UMSS en Cochabamba?",
    category: "Campus",
    emoji: "📍",
  },
  {
    id: 6,
    title: "¿Cómo accedo al sistema SIS de la UMSS?",
    category: "Sistemas",
    emoji: "💻",
  },
  {
    id: 7,
    title: "¿Cuál es el proceso para homologar materias en la UMSS?",
    category: "Trámites",
    emoji: "🔄",
  },
];

export const NewsSidebar: React.FC<NewsSidebarProps> = ({ onSelect }) => {
  const [collapsed, setCollapsed] = useState<boolean>(true);

  return (
    <>
      {collapsed && (
        <button
          className={styles.newsSidebarToggle}
          onClick={() => setCollapsed(false)}
          title="Ver sugerencias"
        >
          <Newspaper size={18} />
        </button>
      )}

      {!collapsed && (
        <div
          className={styles.newsSidebarOverlay}
          onClick={() => setCollapsed(true)}
        />
      )}

      <aside
        className={`${styles.newsSidebar} ${collapsed ? styles['newsSidebar--collapsed'] : ''}`}
      >
        {!collapsed && (
          <>
            <div className={styles.newsSidebarHeader}>
              <button
                className={styles.newsSidebarClose}
                onClick={() => setCollapsed(true)}
                aria-label="Cerrar"
              >
                <X size={18} />
              </button>
              
              <div className={styles.newsSidebarHeaderCenter}>
                <Newspaper size={16} />
                <span className={styles.newsSidebarTitle}>Noticias</span>
              </div>

              <span className={styles.newsSidebarBadge}>{MOCK_NEWS.length}</span>
            </div>

            <ul className={styles.newsSidebarList}>
              {MOCK_NEWS.map((item) => (
                <li
                  key={item.id}
                  className={styles.newsSidebarItem}
                  onClick={() => {
                    onSelect(item.title);
                    setCollapsed(true);
                  }}
                >
                  <div className={styles.newsSidebarItemTop}>
                    <span className={styles.newsSidebarEmoji}>{item.emoji}</span>
                    <span className={styles.newsSidebarCategory}>
                      {item.category}
                    </span>
                  </div>

                  <p className={styles.newsSidebarTitleText}>{item.title}</p>
                  <span className={styles.newsSidebarCta}>Preguntar →</span>
                </li>
              ))}
            </ul>
          </>
        )}
      </aside>
    </>
  );
};

export default NewsSidebar;
