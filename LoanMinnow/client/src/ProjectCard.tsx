// ProjectCard.tsx
import React from 'react';
import './styles/Dashboard.css';


const ProjectCard = ( { label } ) => {
  return (
    <div className="project-card">
        <h3>{label}</h3>
    </div>
  );
};

export default ProjectCard;