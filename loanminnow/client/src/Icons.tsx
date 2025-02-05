// Icons.tsx
import React from 'react';
import './styles/Icons.css';
import { useNavigate } from 'react-router-dom';

const Icons = () => {
  const navigate = useNavigate();

  return (
    <div className="icons-container">
      <div style={{width:10}}></div>
      <button className="icon-btn" onClick={() => navigate('/profile')}>
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