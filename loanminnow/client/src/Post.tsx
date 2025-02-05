import React from "react";
import './styles/FullPage.css';
import './styles/Feed.css'
import './styles/Post.css'
import ProgressBar from "./ProgressBar.tsx";

const Post = ( { name, description, image_url, progress} ) => {
    return (
      <div className="venture-card">
        <img className="venture-image" src={`/api/uploads/${image_url}`}></img>
        <div className="venture-content">
          <h2>{name}</h2>
          <ProgressBar progress={progress} />
          <p>
          {description}
          </p>
        </div>
      </div>
    );
  };
  
  export default Post;
  