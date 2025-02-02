'use client';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Data from './Data.tsx';
import NavBar from './NavBar.tsx';
import NewVenture from './NewVenture.tsx';

export default function CreatePost() {
  return (
    <>
      {/* LANDING PAGE LOGGED IN */}
      <NavBar />
      <div className="container-fluid vh-100 d-flex justify-content-center pt-5" style={{marginTop:60}}>
        <div className="row g-4 w-100">
          <div className="col-12 col-md-8">
            <NewVenture />
          </div>
          <div className="col-12 col-md-4 d-none d-md-block">
            <Data />
          </div>
        </div>
      </div>
    </>
  );
}
