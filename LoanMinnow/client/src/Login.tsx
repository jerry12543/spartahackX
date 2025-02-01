import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

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

    return (
        <div className="login-container">
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
        </div>
    );
};

export default LoginPage;