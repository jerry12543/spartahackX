import React from "react";
import './styles/Feed.css'

const ProgressBar = ({ progress }) => {
  const clampedProgress = Math.min(Math.max(progress, 0), 1);
  const percentage = clampedProgress * 100;

  return (
    <div className="progress-bar">
      <div 
        className="progress" 
        style={{ 
          width: `${percentage}%`,
          background: `linear-gradient(to right, #4caf50, #8bc34a ${percentage}%, #e0e0e0 ${percentage}%)`
        }}
      ></div>
    </div>
  );
}

export default ProgressBar;
