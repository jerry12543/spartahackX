// SearchBar.tsx
import React from 'react';
import './styles/SearchBar.css';
import { useNavigate } from 'react-router-dom';

const SearchBar = () => {
  const navigate = useNavigate();
  
  return (
    <div className="search-bar-container">
      <button className="icon-btn" style={{zIndex:2005}} onClick={() => navigate('/dashboard')}>
        <img 
            src="/static/home.svg" 
            alt="Home"
            className="icon"
            style={{ width:'50px', height:'50px', marginLeft:30, marginTop:5}}
          />
      </button>
      <div className="search-bar" style={{marginLeft:80}}>
        <input type="text" placeholder="Explore ventures..." className="search-input" />
        <button className="search-btn">
        <img 
          src="/static/search.svg" 
          alt="Notifications"
          className="icon notification-icon"
        />
        </button>
      </div>
    </div>
  );
};

export default SearchBar;