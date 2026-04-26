import React, {
  useCallback,
  useEffect,
  useRef,
  useState,
  type KeyboardEvent,
} from "react";
import { useNews } from "../../../hooks/useNews";
import { NewsCard } from "./NewsCard";
import styles from "./NewsCarousel.module.css";

const AUTOPLAY_INTERVAL: number = 6000;

export const NewsCarousel: React.FC<{
  activeChatId?: string | undefined;
  onAsk?: (titulo: string) => void;
}> = ({ activeChatId, onAsk }) => {
  const { news, isLoading, error } = useNews();
  const [activeIndex, setActiveIndex] = useState<number>(0);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const intervalRef: React.MutableRefObject<ReturnType<
    typeof setInterval
  > | null> = useRef(null);
  const prevChatRef = useRef<string | undefined>(undefined);
  const [collapsed, setCollapsed] = useState<boolean>(!!activeChatId);

  useEffect(() => {
    if (prevChatRef.current !== activeChatId) {
      if (prevChatRef.current != null && activeChatId == null) {
        setCollapsed(false);
      } else if (
        prevChatRef.current == null ||
        prevChatRef.current !== activeChatId
      ) {
        if (activeChatId != null) {
          setCollapsed(true);
        }
      }
      prevChatRef.current = activeChatId;
    }
  }, [activeChatId]);

  const total: number = news.length;

  const goTo: (index: number) => void = useCallback(
    (index: number) => {
      setActiveIndex((index + total) % total);
    },
    [total],
  );

  const goNext: () => void = useCallback(() => {
    goTo(activeIndex + 1);
  }, [activeIndex, goTo]);

  const goPrev: () => void = useCallback(() => {
    goTo(activeIndex - 1);
  }, [activeIndex, goTo]);

  useEffect(() => {
    if (isPaused || total <= 1) return;

    intervalRef.current = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % total);
    }, AUTOPLAY_INTERVAL);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPaused, total]);

  function handleKeyDown(e: KeyboardEvent<HTMLElement>): void {
    if (e.key === "ArrowLeft") goPrev();
    if (e.key === "ArrowRight") goNext();
  }

  if (isLoading) {
    return (
      <section className={styles.newsCarousel} aria-label="Cargando noticias">
        <div className={styles.newsCarouselSkeleton}>
          <div className={styles.newsCarouselSkeletonBadge} />
          <div className={styles.newsCarouselSkeletonTitle} />
          <div className={styles.newsCarouselSkeletonLine} />
          <div
            className={`${styles.newsCarouselSkeletonLine} ${styles["newsCarouselSkeletonLine--short"]}`}
          />
        </div>
      </section>
    );
  }

  if (error || total === 0) {
    return null;
  }

  return (
    <section
      className={styles.newsCarousel}
      aria-label="Carrusel de noticias"
      aria-roledescription="carousel"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      onFocus={() => setIsPaused(true)}
      onBlur={() => setIsPaused(false)}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      <header className={styles.newsCarouselHeader}>
        <div className={styles.newsCarouselHeaderLeft}>
          <div className={styles.newsCarouselIcon} aria-hidden="true">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
              <path d="M18 14h-8" />
              <path d="M15 18h-5" />
              <path d="M10 6h8v4h-8V6Z" />
            </svg>
          </div>

          <h2 className={styles.newsCarouselTitle}>Últimas Noticias</h2>
        </div>

        <div className={styles.newsCarouselControls}>
          <button
            className={styles.newsCarouselCollapseBtn}
            onClick={() => setCollapsed((c) => !c)}
            aria-label={collapsed ? "Expandir noticias" : "Colapsar noticias"}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className={`${styles.newsCarouselCollapseIcon} ${collapsed ? styles["newsCarouselCollapseIcon--collapsed"] : ""}`}
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>
        </div>
      </header>

      {!collapsed && (
        <div className={styles.newsCarouselViewport} aria-live="off">
          {news.map((item, index) => (
            <NewsCard
              key={item.id}
              item={item}
              isActive={index === activeIndex}
              onAsk={onAsk}
            />
          ))}
        </div>
      )}

      {!collapsed && (
        <div
          className={styles.newsCarouselDots}
          role="tablist"
          aria-label="Seleccionar noticia"
        >
          {news.map((item, index) => (
            <button
              key={item.id}
              className={`${styles.newsCarouselDot} ${index === activeIndex ? styles["newsCarouselDot--active"] : ""}`}
              onClick={() => goTo(index)}
              role="tab"
              aria-selected={index === activeIndex}
              aria-label={`Noticia ${index + 1} de ${total}`}
            />
          ))}
        </div>
      )}
    </section>
  );
};

export default NewsCarousel;
