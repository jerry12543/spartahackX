// Icons.tsx
import React from 'react';
import './styles/Icons.css';

const Icons = () => {
  return (
    <div className="icons-container">
      <button className="icon-btn">
        <span role="img" aria-label="Notifications">🔔</span>
      </button>
      <div style={{width:10}}></div>
      <button className="icon-btn">
        <span role="img" aria-label="Profile">👤</span>
      </button>
    </div>
  );
};

export default Icons;