import React, {useState, useEffect} from 'react';
import './styles/VentureDetailsI.css';
import NavBar from './NavBar.tsx';
import { useNavigate } from 'react-router-dom';

import { useRef } from 'react';
  
// FROM POV OF PEOPLE WHO WANT TO INVEST

interface Venture {
  id: number;
  name: string;
  description: string;
  goal: number;
  interest_rate: number;
  due_date: string;
  image_url: string;
  pledged_amount: number;
}


// const [pledgeAmount, setPledgeAmount] = useState<number>(0);

const handlePledge = async (venture_id, pledgeAmount) => {
  if (pledgeAmount <= 0) {
    alert("Please enter a valid pledge amount.");
    return;
  }

  try {
    const response = await fetch(`/transactions/ventures/${venture_id}/pledge/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: pledgeAmount })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process pledge');
    }

    const data = await response.json();
    console.log('Pledge successful:', data);

    
  } catch (error) {
    console.error('Error making pledge:', error);
    alert(error instanceof Error ? error.message : 'An error occurred while pledging.');
  }
};



const VentureDetailsI = (venture_id_dict) => {
  const [venture, setVenture] = useState<Venture | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchVentureData = async () => {
    try {
      setIsLoading(true);
      console.log("VentureDetailsI venture_id: ", venture_id_dict['venture_id']);
      const response = await fetch(`/venture/${venture_id_dict['venture_id']}/`, {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch venture data');
      }

      const data: Venture = await response.json();
      console.log("venture data: ", data);
      setVenture(data);
    } catch (err) {
      console.error('Error fetching venture data:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchVentureData();
  }, [])

  if (isLoading) {
    return (
      <>
        <NavBar />
        <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
          <div className="loading">Loading profile...</div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <NavBar />
        <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
          <div className="error-message">Error loading profile: {error}</div>
        </div>
      </>
    );
  }

  return (
    <div className="venture-details-container">
      {/* Venture Name */}
      <h1 className="venture-name">Venture Name</h1>


      <div className="venture-image-container">
        <img className="venture-image" src={'/api/uploads/'+venture.image_url} alt="Venture Image" />
      </div>

      {/* Progress Bar */}
      <progress
        value={venture.pledged_amount ? venture.pledged_amount / venture.goal : 0}
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

      <h1 className="label-style" style={{marginTop:30}}>Goal Amount: {venture.goal}</h1>

      <h1 className="label-style">Interest: {venture.interest_rate}%</h1>

      {/* Due Date */}
      <div className="due-date label-style">
        <label>Due Date:&nbsp;</label>
        <input type="date" value={venture.due_date} readOnly className="due-date-input" />
      </div>

      {/* Description */}
      <div className="description" style={{marginTop:30}}>
        <h3>Description</h3>
        <p>
          {venture.description}
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
      <button className="close-btn" onClick={() => navigate("/dashboard")}>Close</button>
      </div>
    </div>
  );
};

export default VentureDetailsI;