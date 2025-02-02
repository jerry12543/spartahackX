// SearchBar.tsx
import React from 'react';
import './styles/SearchBar.css';

const SearchBar = () => {
  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <img 
          src="/static/search.svg" 
          alt="Notifications"
          className="icon notification-icon"
        />
      </div>
    </div>
  );
};

export default SearchBar;