// SearchBar.tsx
import React from 'react';
import './styles/SearchBar.css';

const SearchBar = () => {
  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <input type="text" placeholder="Search here..." className="search-input" />
        <button className="search-btn">🔍</button>
      </div>
    </div>
  );
};

export default SearchBar;