// Feed.tsx
import React, { useState, useEffect} from 'react';
import './styles/Feed.css';
import Post from './Post.tsx';

interface Venture {
  id: number;
  name: string;
  description: string;
  goal: number;
  interest_rate: number;
  due_date: string;
  image_url: string;
}

interface FeedResponse {
  next: string;
  results: Venture[];
  url: string;
}

const Feed = () => {
  const [ventures, setVentures] = useState<Venture[]>([]);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchVentures = async (url = '/api/venture/newest/') => {
    try {
      setIsLoading(true);
      const response = await fetch(url, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch ventures');
      }

      const data: FeedResponse = await response.json();
      setVentures(prevVentures => [...prevVentures, ...data.results]);
      setNextPage(data.next || null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching ventures:', err);
    } finally {
      setIsLoading(false);
      console.log("Ventures: ", ventures);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchVentures();
  }, []);

  // Load more function for infinite scroll
  const loadMore = () => {
    if (nextPage && !isLoading) {
      fetchVentures(nextPage);
    }
  };

  if (error) {
    return <div className="feed-error">Error loading feed: {error}</div>;
  }

  return (
    <div className="feed-container rounded">
      {ventures.map(venture => (
        <a key={venture.id} href={`/investordetails/${venture.id}`}>
          <Post
            name={venture.name}
            description={venture.description}
            image_url={venture.image_url}
            progress={venture.progress}
          />
        </a>
      ))}
    </div>
  );
};

export default Feed;