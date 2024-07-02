import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './CSS/Home.css';

const Home = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { username } = location.state || {};

  const navigateTo = (path) => {
    navigate(path);
  };

  const navigateToExternal = (url) => {
    window.location.href = url;
  };

  return (
    <div className="container">
      <h2>Home Page</h2>
      <p>Welcome, {username ? username : 'Guest'}!</p>
      <div onClick={() => navigateTo('/build-resume')} className="card">
        <h3>Optimize Resume</h3>
        <p>Start optimizing your professional resume with our easy-to-use tools.</p>
      </div>
      <div onClick={() => navigateTo('/build-cover-letter')} className="card">
        <h3>Build Cover Letter</h3>
        <p>Create a compelling cover letter that highlights your strengths and accomplishments.</p>
      </div>
      <div onClick={() => navigateTo('/prepare-interview')} className="card">
        <h3>Mind Map for your Job</h3>
        <p>Get ready for your interview with our job tips.</p>
      </div>
      <div onClick={() => navigateTo('/job-research')} className="card">
        <h3>Job Research</h3>
        <p>Search for your job.</p>
      </div>
      <div onClick={() => navigateToExternal('http://127.0.0.1:5050/')} className="card">
        <h3>Interview Chat Bot</h3>
        <p>Search for your job.</p>
      </div>
    </div>
  );
};

export default Home;
