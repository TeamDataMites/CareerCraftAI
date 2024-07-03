import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CSS/Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (username) {
      // Save username to session storage
      sessionStorage.setItem('username', username);

      // Navigate to '/home' with username in state
      navigate('/home', { state: { username } });
    } else {
      alert('Please enter a username');
    }
  };

  return (
    <div>
      <div>
        <h1 style={{ textAlign: 'center' }}>Please Log to use our services</h1>
      </div>
      <div>
        <form onSubmit={handleSubmit}>
          <div style={{ backgroundColor: 'tra' }}>
            <label>Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <label>Password:</label>
            <input
              type="password"
              id="password"
            />
          </div>
          <br></br>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
