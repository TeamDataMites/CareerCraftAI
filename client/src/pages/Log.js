import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (username) {
      sessionStorage.setItem('username', username);
      navigate('/home', { state: { username } });
    } else {
      alert('Please enter a username');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Job Interview Support</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={styles.input}
        />
        <label style={styles.label}>Password:</label>
        <input
          type="password"
          id="password"
          style={styles.input}
        />
        <br />
        <button type="submit" style={styles.button}>Login</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#121212', // Dark blue
    color: '#FFFFFF', // White
  },
  header: {
    marginBottom: '20px',
    color: '#BB86FC', // Light purple
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: '#1E1E1E', // Darker blue
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    width: '500px',
  },
  label: {
    marginBottom: '10px',
    color: '#BB86FC', // Light purple
  },
  input: {
    marginBottom: '20px',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #cccccc',
    width: '100%',
    backgroundColor: '#2E2E2E', // Darker gray
    color: '#FFFFFF', // White
  },
  button: {
    padding: '10px 20px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#BB86FC', // Light purple
    color: '#FFFFFF', // White
    cursor: 'pointer',
  },
};


export default Login;
