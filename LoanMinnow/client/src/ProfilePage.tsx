// ProfilePage.tsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './styles/ProfilePage.css';
import './styles/Dashboard.css';
import ProjectCard from './ProjectCard.tsx';
import NavBar from './NavBar.tsx';

interface Venture {
  venture_id: number;
  venture_name: string;
  venture_image_url: string;
  total_pledged: number;
  total_requested: number;
  total_amount_invested_user: number;
}

interface ProfileData {
  username: string;
  score: number;
  available_credits: number;
  credits_invested: number;
  projects: Venture[];
  ventures: Venture[];
}

const ProfilePage = () => {
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [profileData, setProfileData] = useState<ProfileData>({
    username: '',
    score: 0,
    available_credits: 0,
    credits_invested: 0,
    projects: [],
    ventures: []
  });
  const { profile_id } = useParams<{ profile_id: string }>();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfileData = async () => {
    try {
      let url = '/users/profile/';
      if (profile_id) {
        url = '/users/profile/' + profile_id + '/';
      }
      const response = await fetch(url, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch profile data');
      }

      const data = await response.json();
      console.log("receiving this load of data: ", data);
      setProfileData(data);
      console.log('Profile data:', data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Profile fetch error:', err);
    } finally {
      setIsLoading(false);
      console.log('Profile data:', profileData);
    }
  }

  const [goal, setGoal] = useState(0);

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

  useEffect(() => {
    fetchProfileData();
  }, [profile_id]);

  if (isLoading || !profileData) {
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
    <>
    <NavBar />
    <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
      <div className="profile-page-container">
        <div className="profile-header">
          <div className="profile-info">
            <div className="profile-picture-container">
              <div 
                className="profile-picture"
                onClick={() => document.getElementById('profile-upload')?.click()}
                style={{
                  backgroundImage: profileImage ? `url(${profileImage})` : 'none',
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  cursor: 'pointer',
                  width: '150px',
                  height: '150px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <div className="icons-container">
                  {!profileImage && <img className="default-icon" style={{ fontSize: '64px' }} src="/static/user.svg" />}
                </div>
              </div>
              <input
                id="profile-upload"
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={handleImageChange}
              />
            </div>
            <h2 className="username">{profileData.username}</h2>
          </div>
          {/* Credit Info Box */}
          <div className="credit-info-box">
            <div className="row credit-info-row">
                <div className="credit-score-section">
                <span className="credit-score" style={{fontSize:50, paddingLeft:30, marginBottom:-50}}>{profileData.score}</span>
                <div style={{
                  width:36,
                  height:36,
                  backgroundColor:"#4caf50",    // can change color based on reputability here
                  borderRadius:"50%",
                  marginRight:80,
                  marginLeft:10,
                  marginBottom:-50
                  }}></div>

                <div className="col">
                    <div className="d-flex flex-column" style={{fontSize:20}}>
                        <span>Available Credit:</span>
                        <span>${profileData.available_credits}</span>
                    </div>
                </div>

                <div className="col">
                    <div className="d-flex flex-column" style={{fontSize:20}}>
                        <span>Credits Invested:</span>
                        <span>${profileData.credits_invested}</span>
                    </div>
                </div>
                </div>
            </div>
            <div className="d-flex justify-content-end">
              <input
                  type="number"
                  id="goal"
                  min="0"
                  value={goal === 0 ? '' : goal} // Removes "0" placeholder when typing starts
                  onChange={(e) => setGoal(Math.max(0, Number(e.target.value)))}
                  className="form-input"
                  style={{height:40, marginTop:20, marginRight:10, width:"38%"}}
              />
              <button className="add-funds-btn d-flex justify-content-center">Add Funds</button>
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
            {profileData.projects && profileData.projects.length > 0 ? (
              <p>Total Received: ${profileData.projects.reduce((acc, project) => 
                acc + project.total_amount_invested_user, 0).toFixed(2)}</p>
              ) : (
                <p>Total Received: $0</p>
              )}
            {profileData.projects && profileData.projects.length > 0 ? (
                profileData.projects.map((project) => (
                  <ProjectCard
                    venture_id={project.venture_id}
                    label={project.venture_name}
                    percentage={Math.round((project.total_amount_invested_user / project.total_pledged) * 100)}
                    amount={project.total_amount_invested_user}
                  />
                ))
              ) : (
                <p>No projects created yet</p>
              )}
          </div>

          {/* Ventures Section */}
          <div className="col-6">
            <h4>Ventures</h4>
            <p>Total Invested: ${profileData.credits_invested} </p>
            {profileData.ventures && profileData.ventures.length > 0 ? (
              profileData.ventures.map((venture) => (
                <ProjectCard
                venture_id={venture.venture_id}
                label={venture.venture_name}
                percentage={Math.round((venture.total_amount_invested_user / venture.total_requested) * 100)}
                amount={venture.total_amount_invested_user}
                />
              ))
            ) : (
              <p>No ventures created yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default ProfilePage;