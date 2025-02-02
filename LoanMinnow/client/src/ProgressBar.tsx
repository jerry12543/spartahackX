import React from "react";
import './styles/Feed.css'

const ProgressBar = ( { progress } ) => {
    return (
      <div className="progress-bar">
        <div className="progress" style={{ width: `${progress}%` }}></div>
      </div>
    );
  }

export default ProgressBar;