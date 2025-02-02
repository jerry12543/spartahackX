import React from 'react';
import './styles/VentureDetailsI.css';

// FROM POV OF PEOPLE WHO ARE RECEIVING INVESTMENTS

const VentureDetailsC = () => {
  return (
    <div className="venture-details-container">
      {/* Venture Name */}
      <h1 className="venture-name">Venture Name</h1>

      {/* Venture Image */}
      <div className="venture-image-container">
        <div className="venture-image"></div>
      </div>

      {/* Progress Bar */}
      <progress
        value={50 / 100}
        max="1"
        style={{
          width: '100%',
          height: '10px',
          borderRadius: '5px',
          overflow: 'hidden',
          appearance: 'none',
          backgroundColor: '#e0e0e0',
        }}
      />

      <h1 className="label-style" style={{marginTop:30}}>Goal Amount: $10,000</h1>

      <h1 className="label-style">Interest: 5%</h1>

      <h1 className="label-style">Amount Received: $5000</h1>

      {/* Due Date */}
      <div className="due-date label-style">
        <label>Due Date:&nbsp;</label>
        <input type="date" value="2025-02-15" readOnly className="due-date-input" />
      </div>

      {/* Description */}
      <div className="description" style={{marginTop:30}}>
        <h3>Description</h3>
        <p>
          This is a detailed description of the project. It explains what the project is about,
          its purpose, and other important details. It explains what the project is about,
          its purpose, and other important details. It explains what the project is about,
          its purpose, and other important details. It explains what the project is about,
          its purpose, and other important details. It explains what the project is about,
          its purpose, and other important details. It explains what the project is about,
          its purpose, and other important details.
        </p>
      </div>

      {/* Amount Input */}
      <div className="form-group form-row" style={{marginTop:30}}>
        <label htmlFor="amount" className="form-label">Amount</label>
        <input
          type="number"
          id="amount"
          min="0"

          className="form-input"
        />
      </div>

      {/* Buttons */}
      <div className="button-group">
      <button className="close-btn">Close</button>
        <button className="pay-btn">Pay Back</button>
      </div>
    </div>
  );
};

export default VentureDetailsC;