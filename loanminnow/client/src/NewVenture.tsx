// NewVenture.tsx
import React, { useState } from 'react';
import './styles/NewVenture.css';
import { useNavigate } from 'react-router-dom';

const NewVenture = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [interestRate, setInterestRate] = useState(0);
  const [goal, setGoal] = useState(0);
  const [dueDate, setDueDate] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleClick = () => {
    const fileInput = document.getElementById('venture-image') as HTMLInputElement;
    if (fileInput) {
      fileInput.click();
    }
  };

  const submit = async () => {
    try {
      const formData = new FormData();
      formData.append('operation', 'create');
      formData.append('name', name);
      formData.append('interest_rate', interestRate.toString());
      formData.append('goal', goal.toString());
      formData.append('due_date', dueDate);
      formData.append('description', description);
      
      if (selectedFile) {
        formData.append('image', selectedFile);
      }
  
      const response = await fetch("/venture/new/", {
        method: "POST",
        body: formData,
      });
  
      if (response.status === 405) {
        navigate('/');
      }
      if (response.status === 201) {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Venture creation error:', err);
    } finally {
      console.log("Venture created");
    }
  };

  if (error) {
    return <div>Error loading dashboard: {error}</div>;
  }

  return (
    <div className="new-venture-container">
      <h1 className="new-venture-heading">Create a New Venture</h1>

      {/* Custom Image Upload */}
      <div className="form-group">
        <label className="form-label">Upload Image</label>
        <div className="upload-box" onClick={handleClick}>
          {selectedFile ? selectedFile.name : 'Click to upload an image'}
        </div>
        <input
          type="file"
          id="venture-image"
          className="hidden-file-input"
          onChange={handleFileChange}
        />
      </div>

      {/* Name Input */}
      <div className="form-group form-row">
        <label htmlFor="venture-name" className="form-label">Name</label>
        <input
          type="text"
          id="venture-name"
          placeholder="Enter venture name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="form-input"
        />
      </div>

      {/* Interest Rate Input */}
      <div className="form-group form-row">
        <label htmlFor="interest-rate" className="form-label">Interest Rate (%)</label>
        <input
          type="number"
          id="interest-rate"
          min="0"
          value={interestRate === 0 ? '' : interestRate} // Removes "0" placeholder when typing starts
          onChange={(e) => setInterestRate(Number(e.target.value))}
          className="form-input"
        />
      </div>

      {/* Goal Input */}
      <div className="form-group form-row">
        <label htmlFor="goal" className="form-label">Goal ($)</label>
        <input
            type="number"
            id="goal"
            min="0"
            value={goal === 0 ? '' : goal} // Removes "0" placeholder when typing starts
            onChange={(e) => setGoal(Math.max(0, Number(e.target.value)))}
            className="form-input"
        />
        </div>

      {/* Due Date Input */}
      <div className="form-group form-row">
        <label htmlFor="due-date" className="form-label">Due Date</label>
        <input
          type="date"
          id="due-date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="form-input"
        />
      </div>

      {/* Description Input */}
      <div className="form-group">
        <label htmlFor="description" className="form-label">Description</label>
        <textarea
          id="description"
          rows={4}
          placeholder="Enter description..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="form-textarea"
        ></textarea>
      </div>

      {/* FORM BUTTONS */}
      <div className="button-group">
        <button className="cancel-btn" onClick={() => navigate('/dashboard')}>Cancel</button>
        <button className="save-btn" onClick={() => submit()}>Save</button>
    </div>
    </div>
  );
};

export default NewVenture;