import React from "react";
import './styles/FullPage.css';
import './styles/Feed.css'
import './styles/Progress.css';

// progress is whole num from 0-100

const Post = ( { name, description, image_url, progress } ) => {
    return (
      <div className="venture-card">
        <div className="venture-image" src={image_url}></div>
        <div className="venture-content">
          <h2>{name}</h2>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom:'4px', marginTop:'-25px' }}>
          <span style={{ fontSize: '12px', color: '#666' }}>
            {`${progress}% completed`}
          </span>
          </div>

          <progress
            value={progress / 100}
            max="1"
            className="my-progress"
          />

          <p>
          {description}
          </p>
        </div>
      </div>
    );
  };
  
  export default Post;