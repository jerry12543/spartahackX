// DashboardSidebar.tsx
import React from 'react';
import './styles/Dashboard.css';
import ProjectCard from './ProjectCard.tsx';

const Data = () => {
  return (
    <aside className="dashboard-sidebar">
      <div className="score-section">
        <div className="score-display">
          {/* fill in with data from backend */}
          <span className="score-number">750</span>

          <div className="score-indicator"></div>
        </div>
        <div className="credit-info">
          <div className="credit-row">
            <span>Available Credit:</span>

            {/* fill in with data from backend */}
            <span>$1000.00</span>
          </div>
          <div className="credit-row">
            <span>Credits Invested:</span>

            {/* fill in with data from backend */}
            <span>$1000.00</span>
          </div>
        </div>
      </div>

      <div className="projects-section">
        {/* people give u money */}
        <h2>Your Projects</h2> 
        {/* can change names of labels with project names */}
        {/* repeat the card at most 3x */}

        <ProjectCard label={"Project Alpha"}/>
        <ProjectCard label={"Project Beta"}/>
        <ProjectCard label={"Project Gamma"}/>
      </div>

      <div className="projects-section">
        {/* you give other people money */}
        <h2>Your Investments</h2>
        {/* can change names of labels with venture names */}
        {/* repeat the card at most 3x */}

        <ProjectCard label={"Venture Alpha"}/>
        <ProjectCard label={"Venture Beta"}/>
        <ProjectCard label={"Venture Gamma"}/>
      </div>
    </aside>
  );
};

export default Data;