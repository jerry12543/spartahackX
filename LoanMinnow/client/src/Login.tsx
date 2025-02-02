import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles/Login.css';

const LoginPage = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        try {
            e.preventDefault();
            const response = await fetch("/login/",
                {
                    method: 'POST',
                    body: JSON.stringify(formData)
                }
            );

            if (!response.ok) {
                throw new Error('Login failed');
            }
        } catch (err) {
            setError('Login failed. Please try again.');
            console.error('Login error:', err);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const [isLogin, setIsLogin] = useState(true);

    return (


        <div className="vh-100 d-flex justify-content-center">
        <div className="auth-page">
        <div className="auth-left">
          <div className="auth-content">
            <h1>Welcome to LoanMinnow</h1>
            <p>Start your journey with us today</p>
          </div>
        </div>
        
        <div className="auth-right">
          <div className="auth-form-container">
            <h2>{isLogin ? 'Sign In' : 'Create Account'}</h2>
            
            <form className="auth-form">
              {!isLogin && (
                <div className="form-group">
                  <label>Full Name</label>
                  <input type="text" className="auth-input" />
                </div>
              )}
              
              <div className="form-group">
                <label>Email</label>
                <input type="email" className="auth-input" />
              </div>
              
              <div className="form-group">
                <label>Password</label>
                <input type="password" className="auth-input" />
              </div>
  
              <button type="submit" className="auth-button">
                {isLogin ? 'Sign In' : 'Sign Up'}
              </button>
            </form>
  
            <div className="auth-switch">
              {isLogin ? (
                <p>Don't have an account? <span onClick={() => setIsLogin(false)}>Sign up</span></p>
              ) : (
                <p>Already have an account? <span onClick={() => setIsLogin(true)}>Sign in</span></p>
              )}
            </div>
          </div>
        </div>
      </div>
      </div>
    );
};

export default LoginPage;



{/* <div className="login-container">
<h2>Login to Your Account</h2>
<form onSubmit={handleSubmit} className="login-form">
    <div className="form-group">
        <label htmlFor="username">Username:</label>
        <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
        />
    </div>

    <div className="form-group">
        <label htmlFor="password">Password:</label>
        <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
        />
    </div>

    <button type="submit" className="login-button">Log In</button>
</form>

<div className="signup-link">
    Don't have an account? <a href="/signup">Sign up here</a>
</div>
{error && <div className="error-message">{error}</div>}
</div> */}
