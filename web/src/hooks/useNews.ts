import { useState, useEffect, useCallback } from 'react';

export interface NewsItem {
  id: number;
  title: string;
  summary: string;
  content: string;
  category: string;
  post_date: string;
}

interface UseNewsReturn {
  news: NewsItem[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useNews(): UseNewsReturn {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNews = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/content/');

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data: NewsItem[] = await response.json();
      const newsItems = data
        .filter((item) => item.category === 'NEW')
        .sort((a, b) => new Date(b.post_date).getTime() - new Date(a.post_date).getTime())
        .slice(0, 4);

      setNews(newsItems);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
      setNews([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  return { news, isLoading, error, refetch: fetchNews };
}
