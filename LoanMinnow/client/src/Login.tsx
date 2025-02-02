import React, { useState } from 'react';
import './styles/Login.css';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        name: ''
    });
    const [error, setError] = useState("");
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Form data:', formData);
        if (!formData.email || !formData.password || (!isLogin && !formData.name)) {
            setError('Please fill in all fields');
            return;
        }
        try {
            const response = await fetch(isLogin ? "/auth/login/" : "/auth/signup/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            if (response.status === 200) {
                setError(isLogin ? 'Login successful' : 'Sign up successful');
                navigate('/dashboard');
            }
            else if (response.status === 409) {
                setError(isLogin ? "Incorrect password" : "Email already exists, please sign in");
            }
            else if (response.status === 400 && isLogin) {
                setError("Email not found, please sign up");
            }
            else {
                setError(isLogin ? 'Sign in failed' : 'Sign up failed');
            }
        } catch (err) {
            setError(err.message);
            console.error('Error:', err);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

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
                        {error && <div className="error-message">{error}</div>}
                        
                        <form onSubmit={handleSubmit}>
                            {!isLogin && (
                                <div className="form-group">
                                    <label>Full Name</label>
                                    <input 
                                        type="text" 
                                        className="auth-input" 
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                    />
                                </div>
                            )}
                            
                            <div className="form-group">
                                <label>Email</label>
                                <input 
                                    type="text" 
                                    className="auth-input" 
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                />
                            </div>
                            
                            <div className="form-group">
                                <label>Password</label>
                                <input 
                                    type="password" 
                                    className="auth-input" 
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                />
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
