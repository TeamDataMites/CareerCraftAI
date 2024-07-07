import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

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
      <div style={{backgroundColor:'#1E1E1E',padding:'1%'}}>
          <h1 style={{color:'#BB86FC'}}>Ready4urInterview</h1>
          <p style={styles.welcome}>Welcome, {username ? username : 'Guest'}!</p>
      </div>
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <h2 style={styles.header}>Recommended Jobs</h2>
        {Object.keys(recommends).length > 0 ? (
          Object.keys(recommends).map((key) => (
            <div key={key} style={styles.jobitem} onClick={() => window.open(recommends[key]["Job Link"], '_blank')}>
              <h3 style={styles.jobTitle}>{recommends[key]["Job Title"]}</h3>
              <p style={styles.company}>{recommends[key]["Company"]}</p>
            </div>
          ))
        ) : (
          <p style={styles.noRecommendations}>
            {Object.keys(recommends).length === 0 && "No recommendations available."}
          </p>
        )}
      </div>
      <div style={styles.mainContent}>
        <h2 style={styles.header}>Our Services</h2>
        <div style={{display:'flex',flexWrap:'wrap'}}>
          <div onClick={() => navigateTo('/build-resume')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Optimize Resume</h3>
            <p style={styles.serviceDescription}>Start optimizing your professional resume with our easy-to-use tools.</p>
          </div>
          <div onClick={() => navigateTo('/build-cover-letter')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Build Cover Letter</h3>
            <p style={styles.serviceDescription}>Create a compelling cover letter that highlights your strengths and accomplishments.</p>
          </div>
          <div onClick={() => navigateTo('/prepare-interview')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Mind Map for your Dream Job</h3>
            <p style={styles.serviceDescription}>Get ready for your interview with our job tips.</p>
          </div>
          <div onClick={() => navigateTo('/job-research')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Job Research</h3>
            <p style={styles.serviceDescription}>Search for your job.</p>
          </div>
          <div onClick={() => navigateToExternal('http://127.0.0.1:5050/')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Interview Chat Bot</h3>
            <p style={styles.serviceDescription}>Preparation questions</p>
          </div>
          <div onClick={() => navigateToExternal('/lecture-note')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Lecture Notes</h3>
            <p style={styles.serviceDescription}>Prepare a lecture note for your job domain</p>
          </div>
          <div onClick={() => navigateTo('/help-desk')} style={styles.service}>
            <h3 style={styles.serviceTitle}>Get Help</h3>
            <p style={styles.serviceDescription}>Ai powered Helpdesk ready to assist you.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'flex-start',
    backgroundColor: '#121212',
    color: '#FFFFFF',
    height: '100vh',
    marginTop: '-21px',
  },
  sidebar: {
    width: '360px',
    padding: '20px',
    backgroundColor: '#1E1E1E',
  },
  header: {
    color: '#BB86FC',
  },
  jobitem: {
    backgroundColor: '#2E2E2E',
    padding: '10px',
    margin: '10px 0',
    borderRadius: '5px',
    cursor: 'pointer',
    border: '1px solid #BB86FC',
  },
  jobTitle: {
    color: '#BB86FC',
  },
  company: {
    color: '#FFFFFF',
  },
  noRecommendations: {
    textAlign: 'center',
    color: '#BB86FC',
  },
  mainContent: {
    flex: 1,
    padding: '20px',
  },
  welcome: {
    color: '#BB86FC',
  },
  services: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  service: {
    backgroundColor: '#2E2E2E',
    padding: '10px',
    margin: '10px',
    borderRadius: '5px',
    cursor: 'pointer',
    width: '400px',
    height: '100px',
    border: '1px solid #BB86FC',
  },
  serviceTitle: {
    color: '#BB86FC',
  },
  serviceDescription: {
    color: '#FFFFFF',
  },
};

export default Home;
