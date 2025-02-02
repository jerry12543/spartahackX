import React from "react";
import './styles/FullPage.css';
import './styles/Feed.css'

const Post = ( { name, description } ) => {
    return (
      <div className="venture-card">
        <div className="venture-image"></div>
        <div className="venture-content">
          <h2>{name}</h2>
          <div className="progress-bar">
            <div className="progress" style={{ width: '80%' }}></div>
          </div>
          <p>
          {description}
          </p>
        </div>
      </div>
    );
  };
  
  export default Post;
  