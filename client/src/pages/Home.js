import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './CSS/Home.css';

const Home = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { username } = location.state || {};
  const [recommends, setRecommends] = useState({});

  // Function to fetch recommendations based on indexes
  const getRecommendations = async (indexes) => {
    const url = "http://localhost:8082/server/recommendations";

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          indexes: indexes
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setRecommends(data || {});
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommends({});
    }
  };

  // Function to call semantic search based on query
  const callSemanticSearch = async (query) => {
    const url = "http://localhost:8084/search";

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: query,
          top_k: 10
        })
      });

      if (!response.ok) {
        throw new Error('Failed to perform semantic search');
      }

      const data = await response.json();
      console.log(data.indexes);
      await getRecommendations(data.indexes);
    } catch (error) {
      console.error('Error performing semantic search:', error);
      setRecommends({});
    }
  };

  // Function to fetch search results from DB and initiate semantic search
  const fetchFromDB = async () => {
    const url = "http://localhost:8082/server/retrievesearches";

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }

      const data = await response.json();
      console.log(data.search_results);
      await callSemanticSearch(data.search_results);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setRecommends({});
    }
  };

  // Fetch data from DB on component mount
  useEffect(() => {
    if (username) {
      fetchFromDB();
    }
  }, [username]);

  // Function to navigate within the app
  const navigateTo = (path) => {
    navigate(path);
  };

  // Function to navigate to external URL
  const navigateToExternal = (url) => {
    window.open(url, '_blank');
  };

  return (
    <div>
      <div>
        <h1 style={{ textAlign: 'center' }}>Welcome, {username ? username : 'Guest'}!</h1>
      </div>
      <br />
      <h3 style={{ textAlign: 'center' }}>Jobs Recommended For You</h3>
      <div className="container1">
        {Object.keys(recommends).length > 0 ? (
          Object.keys(recommends).map((key) => (
            <div key={key} className="job-item" onClick={() => window.open(recommends[key]["Job Link"], '_blank')}>
              <h3>{recommends[key]["Job Title"]}</h3>
              <p>{recommends[key]["Company"]}</p>
            </div>
          ))
        ) : (
          <p style={{ textAlign: 'center' }}>
            {Object.keys(recommends).length === 0 && "No recommendations available."}
          </p>
        )}
      </div>
      <h3 style={{ textAlign: 'center' }}>Our Services For You</h3>
      <div className="container1">
        <div onClick={() => navigateTo('/build-resume')} className="card">
          <h3>Optimize Resume</h3>
          <p>Start optimizing your professional resume with our easy-to-use tools.</p>
        </div>
        <div onClick={() => navigateTo('/build-cover-letter')} className="card">
          <h3>Build Cover Letter</h3>
          <p>Create a compelling cover letter that highlights your strengths and accomplishments.</p>
        </div>
        <div onClick={() => navigateTo('/prepare-interview')} className="card">
          <h3>Mind Map for your Dream Job</h3>
          <p>Get ready for your interview with our job tips.</p>
        </div>
        <div onClick={() => navigateTo('/job-research')} className="card">
          <h3>Job Research</h3>
          <p>Search for your job.</p>
        </div>
        <div onClick={() => navigateToExternal('http://127.0.0.1:5050/')} className="card">
          <h3>Interview Chat Bot</h3>
          <p>Preparation questions</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
