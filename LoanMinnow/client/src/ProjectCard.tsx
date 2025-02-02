// ProjectCard.tsx
import React from 'react';
import { Link } from 'react-router-dom';

import './styles/Dashboard.css';

interface ProjectCardProps {
  label: string;
  ventureId: number;  // Add this prop for the link
  amount?: number;    // Optional amount to display
}

const ProjectCard = ( { label, venture_id } ) => {
  return (
    <Link to={`/venture/${venture_id}`} className="project-card-link">
      <div className="project-card">
          <h3>{label}</h3>
      </div>
    </Link>
  );
};

export default ProjectCard;
