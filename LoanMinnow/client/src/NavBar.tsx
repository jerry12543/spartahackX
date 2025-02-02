// NavBar.tsx
import React from 'react';
import './styles/NavBar.css';
import VentureButton from './VentureButton.tsx';
import Icons from './Icons.tsx';
import SearchBar from './SearchBar.tsx';

const NavBar = () => {
  return (
    <div className="nav-bar-container">
      <div className="logo-container">
        <img src="/static/home.svg" alt="LoanMinnow" className="logo" />
      </div>
      <div className="search-bar">
        <SearchBar />
      </div>
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