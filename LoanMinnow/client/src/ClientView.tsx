'use client';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import DashboardSidebar from './Data.tsx';
import NavBar from './NavBar.tsx';
import VentureDetailsC from './VentureDetailsC.tsx';

export default function ClientView() {
  return (
    <>
      {/* LANDING PAGE LOGGED IN */}
      <NavBar />
      <div className="container-fluid vh-100 d-flex justify-content-center pt-5" style={{marginTop:60}}>
        <div className="row g-4 w-100">
          <div className="col-12 col-md-8">
            <VentureDetailsC />
          </div>
          <div className="col-12 col-md-4 d-none d-md-block">
            <DashboardSidebar />
          </div>
        </div>
      </div>
    </>
  );
}
