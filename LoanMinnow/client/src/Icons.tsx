// Icons.tsx
import React from 'react';
import './styles/Icons.css';
// import { bellIcon, userIcon } from './../static/bell.svg'

const Icons = () => {
  return (
    <div className="icons-container">
      <button className="icon-btn">
        <img 
          src="/static/bell.svg" 
          alt="Notifications"
          className="icon notification-icon"
        />
      </button>
      <div style={{width:10}}></div>
      <button className="icon-btn">
        <img 
            src="/static/user.svg" 
            alt="Notifications"
            className="icon notification-icon"
          />
      </button>
    </div>
  );
};

export default Icons;