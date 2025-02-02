'use client';
import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import DashboardSidebar from './Data.tsx';
import NavBar from './NavBar.tsx';
import VentureDetailsI from './VentureDetailsI.tsx';
import { UNSAFE_useFogOFWarDiscovery, useParams } from 'react-router-dom';
import App from './index.tsx';


const InvestorView = () => {
  const { venture_id } = useParams<{ venture_id: string }>();
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [ventureData, setVentureData] = React.useState({
    venture_name: '',
    venture_image_url: '',
    total_pledged: 0,
    total_requested: 0,
    total_amount_invested_user: 0
  });

  const fetchVentureData = async () => {
    try{
      if (!venture_id) {
        return <div>No venture ID provided</div>;
      }
      
      console.log("InvestorView venture_id: ", venture_id);
      let url = `/venture/${venture_id}/`;
      const response = await fetch(url, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch venture data');
      }

      const data = await response.json();
      console.log("receiving this load of data: ", data);
      setVentureData(data);
      console.log('Venture data:', data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Venture Data fetch error:', err);
    } finally {
      setLoading(false);
      console.log('Venture Data data:', ventureData);
    }
  }

  useEffect(() => {
    fetchVentureData();
  }, []);

  if (loading) {
    return (
      <>
        <NavBar />
        <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
          <div className="loading">Loading venture data...</div>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <NavBar />
        <div className="container-fluid d-flex justify-content-center pt-5" style={{marginTop:60}}>
          <div className="error-message">Error loading venture: {error}</div>
        </div>
      </>
    );
  }

  return (
    <>
      {/* LANDING PAGE LOGGED IN */}
      <NavBar />
      <div className="container-fluid vh-100 d-flex justify-content-center pt-5" style={{marginTop:60}}>
        <div className="row g-4 w-100">
          <div className="col-12 col-md-8">
            <VentureDetailsI venture_id={venture_id}/>
          </div>
          <div className="col-12 col-md-4 d-none d-md-block">
            <DashboardSidebar />
          </div>
        </div>
      </div>
    </>
  );
}

export default InvestorView;