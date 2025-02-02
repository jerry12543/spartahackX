// Icons.tsx
import React from 'react';
import './styles/Icons.css';
// import { bellIcon, userIcon } from './../static/bell.svg'

const Icons = () => {
  return (
    <div className="icons-container">
      <div style={{width:10}}></div>
      <button className="icon-btn">
        <img 
            src="/static/user.svg" 
            alt="User"
            className="icon"
            style={{ width:'40px', height:'40px' }}
          />
      </button>
    </div>
  );
};

export default Icons;