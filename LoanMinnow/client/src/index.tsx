import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import LoginPage from "./Login.tsx"
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  return (
    <div className="app">
      <LoginPage />
    </div>
  );
};

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
