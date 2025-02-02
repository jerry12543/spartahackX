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
      const url = '/users/profile/' + profile_id + '/';
      const response = await fetch(url, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch profile data');
      }

      const data = await response.json();
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
  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <>
    <NavBar />
    <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
    <div className="profile-page-container">
      <div className="profile-header">
        <div className="profile-info">
          <div className="profile-picture-container">
            <img
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
            </img>
          </div>
          <h2 className="username">user_name</h2>
        </div>

        {/* Credit Info Box */}
        <div className="credit-info-box">
        <div className="row credit-info-row">
            <div className="credit-score-section">
            <span className="credit-score" style={{fontSize:50, paddingLeft:30, marginBottom:-50}}>750</span>
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
    </div>
    </>
  );
};

export default ProfilePage;