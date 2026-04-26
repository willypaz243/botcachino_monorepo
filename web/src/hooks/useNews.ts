import { useState, useEffect, useCallback } from 'react';
import type { NewsItem } from '../types/api.types';
import type { UseNewsReturn } from '../types/hooks.types';

export function useNews(): UseNewsReturn {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNews: () => Promise<void> = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response: Response = await fetch('/api/content/', {
        headers: { 'X-API-Key': import.meta.env.VITE_API_KEY || '' },
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data: NewsItem[] = await response.json();
      
      const newsItems: NewsItem[] = data
        .filter((item: NewsItem) => item.category === 'NEW')
        .sort((a: NewsItem, b: NewsItem) => 
          new Date(b.post_date).getTime() - new Date(a.post_date).getTime()
        )
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

export default useNews;
