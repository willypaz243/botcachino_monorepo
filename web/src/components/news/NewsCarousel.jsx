import { useState, useEffect, useCallback, useRef } from 'react';
import { useNews } from '../../hooks/useNews';
import NewsCard from './NewsCard';
import './NewsCarousel.css';

const AUTOPLAY_INTERVAL = 6000;

export default function NewsCarousel() {
  const { news, isLoading, error } = useNews();
  const [activeIndex, setActiveIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const intervalRef = useRef(null);

  const total = news.length;

  const goTo = useCallback((index) => {
    setActiveIndex((index + total) % total);
  }, [total]);

  const goNext = useCallback(() => {
    goTo(activeIndex + 1);
  }, [activeIndex, goTo]);

  const goPrev = useCallback(() => {
    goTo(activeIndex - 1);
  }, [activeIndex, goTo]);

  useEffect(() => {
    if (isPaused || total <= 1) return;

    intervalRef.current = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % total);
    }, AUTOPLAY_INTERVAL);

    return () => clearInterval(intervalRef.current);
  }, [isPaused, total]);

  function handleKeyDown(e) {
    if (e.key === 'ArrowLeft') goPrev();
    if (e.key === 'ArrowRight') goNext();
  }

  if (isLoading) {
    return (
      <section className="news-carousel" aria-label="Cargando noticias">
        <div className="news-carousel-skeleton">
          <div className="news-carousel-skeleton-badge" />
          <div className="news-carousel-skeleton-title" />
          <div className="news-carousel-skeleton-line" />
          <div className="news-carousel-skeleton-line news-carousel-skeleton-line--short" />
        </div>
      </section>
    );
  }

  if (error || total === 0) {
    return null;
  }

  return (
    <section
      className="news-carousel"
      aria-label="Carrusel de noticias"
      aria-roledescription="carousel"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      onFocus={() => setIsPaused(true)}
      onBlur={() => setIsPaused(false)}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      <header className="news-carousel-header">
        <div className="news-carousel-header-left">
          <div className="news-carousel-icon" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
              <path d="M18 14h-8" />
              <path d="M15 18h-5" />
              <path d="M10 6h8v4h-8V6Z" />
            </svg>
          </div>
          <h2 className="news-carousel-title">Últimas Noticias</h2>
        </div>

        <div className="news-carousel-controls">
          <button
            className="news-carousel-btn"
            onClick={goPrev}
            aria-label="Noticia anterior"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>

          <span className="news-carousel-counter" aria-live="polite">
            {activeIndex + 1} / {total}
          </span>

          <button
            className="news-carousel-btn"
            onClick={goNext}
            aria-label="Siguiente noticia"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 6 15 12 9 18" />
            </svg>
          </button>
        </div>
      </header>

      <div className="news-carousel-viewport" aria-live="off">
        {news.map((item, index) => (
          <NewsCard key={item.id} item={item} isActive={index === activeIndex} />
        ))}
      </div>

      <div className="news-carousel-dots" role="tablist" aria-label="Seleccionar noticia">
        {news.map((item, index) => (
          <button
            key={item.id}
            className={`news-carousel-dot ${index === activeIndex ? 'news-carousel-dot--active' : ''}`}
            onClick={() => goTo(index)}
            role="tab"
            aria-selected={index === activeIndex}
            aria-label={`Noticia ${index + 1} de ${total}`}
          />
        ))}
      </div>
    </section>
  );
}
