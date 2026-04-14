import { useState } from "react";
import "./NewsSidebar.css";

const MOCK_NOTICIAS = [
  {
    id: 1,
    titulo:
      "¿Cuáles son los requisitos para inscribirse a Ingeniería de Sistemas?",
    categoria: "Inscripciones",
    emoji: "📋",
  },
  {
    id: 2,
    titulo: "¿Cuándo empieza el calendario académico 2025?",
    categoria: "Académico",
    emoji: "📅",
  },
  {
    id: 3,
    titulo: "¿Cómo obtengo mi certificado de notas en la UMSS?",
    categoria: "Trámites",
    emoji: "📄",
  },
  {
    id: 4,
    titulo: "¿Qué facultades ofrece la Universidad Mayor de San Simón?",
    categoria: "Facultades",
    emoji: "🏛️",
  },
  {
    id: 5,
    titulo: "¿Dónde queda el campus central de la UMSS en Cochabamba?",
    categoria: "Campus",
    emoji: "📍",
  },
  {
    id: 6,
    titulo: "¿Cómo accedo al sistema SIS de la UMSS?",
    categoria: "Sistemas",
    emoji: "💻",
  },
  {
    id: 7,
    titulo: "¿Cuál es el proceso para homologar materias en la UMSS?",
    categoria: "Trámites",
    emoji: "🔄",
  },
];
export default function NewsSidebar({ onSelect }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`news-sidebar ${collapsed ? "news-sidebar--collapsed" : ""}`}
    >
      <button
        className="news-sidebar-toggle"
        onClick={() => setCollapsed(!collapsed)}
        title={collapsed ? "Expandir noticias" : "Colapsar noticias"}
      >
        {collapsed ? "📰" : "✕"}
      </button>

      {!collapsed && (
        <>
          <div className="news-sidebar-header">
            <span className="news-sidebar-title">📰 Noticias</span>
            <span className="news-sidebar-badge">{MOCK_NOTICIAS.length}</span>
          </div>
          <ul className="news-sidebar-list">
            {MOCK_NOTICIAS.map((noticia) => (
              <li
                key={noticia.id}
                className="news-sidebar-item"
                onClick={() => onSelect(noticia.titulo)}
              >
                <div className="news-sidebar-item-top">
                  <span className="news-sidebar-emoji">{noticia.emoji}</span>
                  <span className="news-sidebar-categoria">
                    {noticia.categoria}
                  </span>
                </div>
                <p className="news-sidebar-titulo">{noticia.titulo}</p>
                <span className="news-sidebar-cta">Preguntar →</span>
              </li>
            ))}
          </ul>
        </>
      )}
    </aside>
  );
}
