import './NewsCard.css';

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString('es-BO', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export default function NewsCard({ item, isActive }) {
  return (
    <article
      className={`news-card ${isActive ? 'news-card--active' : ''}`}
      aria-hidden={!isActive}
    >
      <div className="news-card-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
          <path d="M18 14h-8" />
          <path d="M15 18h-5" />
          <path d="M10 6h8v4h-8V6Z" />
        </svg>
        Noticia
      </div>

      <h3 className="news-card-title">{item.title}</h3>
      <p className="news-card-summary">{item.summary}</p>

      <footer className="news-card-footer">
        <time className="news-card-date" dateTime={item.post_date}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          {formatDate(item.post_date)}
        </time>
      </footer>
    </article>
  );
}
