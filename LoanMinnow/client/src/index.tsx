import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import LoginPage from "./Login.tsx"
import Dashboard from './Dashboard.tsx';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import CreatePost from './CreatePost.tsx';
import ProfilePage from './ProfilePage.tsx';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/newventure" element={<CreatePost />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </BrowserRouter>
  );
};

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
