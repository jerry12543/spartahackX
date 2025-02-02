// NavBar.tsx
import React from 'react';
import './styles/NavBar.css';
import VentureButton from './VentureButton.tsx';
import Icons from './Icons.tsx';
import SearchBar from './SearchBar.tsx';

const NavBar = () => {
  return (
    <div className="nav-bar-container">
      <div className="search-bar">
        <SearchBar />
      </div>
      <div className="nav-actions">
        <VentureButton />
        <div style={{width:250}}></div>
        <Icons />
      </div>
    </div>
  );
};

export default NavBar;