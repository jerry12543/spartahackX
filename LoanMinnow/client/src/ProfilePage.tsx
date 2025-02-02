// ProfilePage.tsx
import React, { useState } from 'react';
import './styles/ProfilePage.css';
import './styles/Dashboard.css';
import ProjectCard from './ProjectCard.tsx';

const ProfilePage = () => {
  const [profileImage, setProfileImage] = useState<string | null>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        setProfileImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="profile-page-container">
      {/* Profile Header */}
      <div className="profile-header">
        {/* Profile Picture and Username */}
        <div className="profile-info">
          <div className="profile-picture-container">
            <div
              className="profile-picture"
              style={{
                backgroundImage: `url(${profileImage || ''})`,
              }}
            >
              {!profileImage && <span className="default-icon">👤</span>}
              <input
                type="file"
                accept="image/*"
                className="hidden-file-input"
                onChange={handleImageChange}
              />
            </div>
          </div>
          <h2 className="username">user_name</h2>
        </div>

        {/* Credit Info Box */}
        <div className="credit-info-box">
        <div className="row credit-info-row">
            <div className="credit-score-section">
            <span className="credit-score" style={{fontSize:30, paddingLeft:30}}>750</span>
            <div className="green-dot"></div>

            <div className="col">
                <div className="d-flex flex-column" style={{fontSize:20}}>
                    <span>Available Credit:</span>
                    <span>$1000.00</span>
                </div>
            </div>

            <div className="col">
                <div className="d-flex flex-column" style={{fontSize:20}}>
                    <span>Credits Invested:</span>
                    <span>$1000.00</span>
                </div>
            </div>
            </div>
            <div className="credit-amounts">
            
            </div>
        </div>
        <div className="d-flex justify-content-end">
        <button className="add-funds-btn d-flex justify-content-center w-100">Add Funds</button>
        </div>
        
        </div>
        
      </div>

      {/* Account Activity */}
      <div className="pt-3">
      <h1 className="account-activity-heading">Account Activity</h1>
      </div>

      {/* Projects and Ventures Section */}
      <div className="row g-4 w-100 projects-ventures-container rounded p-3"
            style={{marginTop:30}}>

        {/* Projects Section */}
        <div className="col-6">
          <h4>Projects</h4>
          <p>Total Received: $5000</p>
          <ProjectCard venture_id={""} label={"Project 1"} percentage={50} amount={500}/>
          <ProjectCard venture_id={""} label={"Project 2"} percentage={5} amount={500}/>
          <ProjectCard venture_id={""} label={"Project 3"} percentage={5} amount={500}/>
          <ProjectCard venture_id={""} label={"Project 4"} percentage={5} amount={500}/>
        </div>

        {/* Ventures Section */}
        <div className="col-6">
          <h4>Ventures</h4>
          <p>Total Invested: $5000</p>
          <ProjectCard venture_id={""} label={"Venture 1"} percentage={5} amount={500}/>
          <ProjectCard venture_id={""} label={"Venture 2"} percentage={5} amount={500}/>
          <ProjectCard venture_id={""} label={"Venture 3"} percentage={5} amount={500}/>
          <ProjectCard venture_id={""} label={"Venture 4"} percentage={5} amount={500}/>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;