// StartVentureButton.tsx
import React from 'react';
import './styles/VentureButton.css';
import { useNavigate } from 'react-router-dom';

const VentureButton = () => {
  const navigate = useNavigate();
  return (
    <button className="start-venture-btn" onClick={() => navigate('/newventure')}>Start Venture</button>
  );
};

export default VentureButton;