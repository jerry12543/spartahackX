import React, {useState, useEffect} from 'react';
import './styles/VentureDetailsI.css';
import NavBar from './NavBar.tsx';

// FROM POV OF PEOPLE WHO WANT TO INVEST

interface Venture {
  id: number;
  name: string;
  description: string;
  goal: number;
  interest_rate: number;
  due_date: string;
  image_url: string;
}

const VentureDetailsI = (venture_id_dict) => {
  const [venture, setVenture] = useState<Venture | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

      {/* Venture Image */}
      <div className="venture-image-container">
        <div className="venture-image">
          <img src={'/api/uploads/'+venture.image_url} alt="Venture Image" />
        </div>
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
        <button className="pay-btn">Pay</button>
      </div>
    </div>
  );
};

export default VentureDetailsI;