import React from 'react';
import './styles/SearchBar.css';
import { useNavigate } from 'react-router-dom';

const SearchBar = () => {
  const navigate = useNavigate();
  
  return (
    <div className="search-bar-container">
      <button className="icon-btn" style={{zIndex:2005}} onClick={() => navigate('/dashboard')}>
        <img 
          src="/static/search.svg" 
          alt="Notifications"
          className="icon notification-icon"
        />
      </button>
    </div>
  );
};
export default SearchBar;
