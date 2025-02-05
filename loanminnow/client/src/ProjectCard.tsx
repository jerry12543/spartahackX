// ProjectCard.tsx
import React from 'react';
import { Link } from 'react-router-dom';

import './styles/Dashboard.css';
import './styles/Progress.css'; 

interface ProjectCardProps {
  label: string;
  ventureId: number;  // Add this prop for the link
  amount?: number;    // Optional amount to display
}

const ProjectCard = ( { label, venture_id, percentage, amount } ) => {
  return (
    <Link to={`/venture/${venture_id}`} className="project-card-link">
      <div className="project-card" style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', width: '100%' }}>
      <div className="card-header" style={{ marginBottom: '10px' }}>
        <h3 style={{ margin: 0 }}>{label}</h3>
        <span style={{ fontSize: '14px', color: '#666' }}>{`${percentage}%`}</span>
      </div>
      <progress
        value={percentage / 100}
        max="1"
        className="my-progress"
      />
      <div className="divider" style={{ margin: '10px 0', height: '1px', backgroundColor: '#ccc' }}></div>
      <span style={{ fontSize: '16px', fontWeight: 'bold' }}>{`$${amount}`}</span>
    </div>
    </Link>
  );
};


export default ProjectCard;
