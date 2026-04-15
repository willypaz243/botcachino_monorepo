import { useState, useEffect, useCallback } from 'react';

export function useNews() {
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchNews = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/content');

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      const newsItems = data
        .filter((item) => item.category === 'NEW')
        .sort((a, b) => new Date(b.post_date) - new Date(a.post_date));

      setNews(newsItems);
    } catch (err) {
      setError(err.message);
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
