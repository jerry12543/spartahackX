// NavBar.tsx
import React from 'react';
import './styles/NavBar.css';
import VentureButton from './VentureButton.tsx';
import Icons from './Icons.tsx';
import { useNavigate } from 'react-router-dom';

const NavBar = () => {
  const navigate = useNavigate();
  return (
    <div className="nav-bar-container">
      <button className="icon-btn" onClick={() => navigate('/dashboard')}>
        <img src="/static/home.svg" alt="LoanMinnow" className="logo" fill="#4b5563"/>
      </button>
      <div className="nav-actions">
        <VentureButton />
        <div className="icons-container">
          <Icons />
        </div>
      </div>
    </div>
  );
};

export default NavBar;