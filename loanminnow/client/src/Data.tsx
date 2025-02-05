// DashboardSidebar.tsx
import React from 'react';
import { useState, useEffect } from 'react';
import './styles/Dashboard.css';
import ProjectCard from './ProjectCard.tsx';
import { useNavigate } from 'react-router-dom';


interface Venture {
  venture_id: number;
  venture_name: string;
  venture_image_url: string;
  total_pledged: number;
  total_requested: number;
  total_amount_invested_user: number;
}

interface DashboardData {
  score: number;
  available_credits: number;
  credits_invested: number;
  top_supported: Venture[];
  top_created: Venture[];
}

const DashboardSidebar = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    score: 0,
    available_credits: 0,
    credits_invested: 0,
    top_supported: [],
    top_created: []
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('/api/dashboard/', {
          credentials: 'include'
        });
        
        if (response.status === 405) {
          navigate('/');
        }

        if (!response.ok) {
          throw new Error('Failed to fetch dashboard data');
        }
        
        const data = await response.json();
        setDashboardData(data);
        console.log('Dashboard data:', data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Dashboard fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return <div>Loading dashboard...</div>;
  }

  if (error) {
    return <div>Error loading dashboard: {error}</div>;
  }

  return (
    <aside className="dashboard-sidebar">
      <div className="score-section">
        <div className="score-display">
          <span className="score-number">{dashboardData.score}</span>
          <div className="score-indicator"></div>
        </div>
        <div className="credit-info">
          <div className="credit-row">
            <span>Available Credit:</span>

            <span>{dashboardData.available_credits}</span>
          </div>
          <div className="credit-row">
            <span>Credits Invested:</span>
            <span>{dashboardData.credits_invested}</span>
          </div>
        </div>
      </div>

      <div className="projects-section">
        <h2>Your Projects</h2> 
        {dashboardData.top_created.map((venture) => {
          <ProjectCard venture_id={venture.venture_id} label={venture.venture_name} percentage={venture.percentage} amount={venture.amount}/>
        })}
      </div>

      <div className="projects-section">
        <h2>Your Investments</h2>
        {dashboardData.top_supported.map((venture) => {
          <ProjectCard venture_id={venture.venture_id} label={venture.venture_name} percentage={venture.percentage} amount={venture.amount}/>
        })}
      </div>
    </aside>
  );
};

export default DashboardSidebar;