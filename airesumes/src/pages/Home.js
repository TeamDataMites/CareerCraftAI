import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const navigateTo = (path) => {
    navigate(path);
  };

  return (
    <div>
      <h2>Home Page</h2>
      <p>Welcome to the Home page!</p>
      <div onClick={() => navigateTo('/build-resume')} style={{ cursor: 'pointer', marginBottom: '10px' }}>
        <h3>Build Resume</h3>
        <p>Start building your professional resume with our easy-to-use tools.</p>
      </div>
      <div onClick={() => navigateTo('/build-cover-letter')} style={{ cursor: 'pointer', marginBottom: '10px' }}>
        <h3>Build Cover Letter</h3>
        <p>Create a compelling cover letter that highlights your strengths and accomplishments.</p>
      </div>
      <div onClick={() => navigateTo('/prepare-interview')} style={{ cursor: 'pointer' }}>
        <h3>Prepare Your Interview</h3>
        <p>Get ready for your interview with our preparation guides and tips.</p>
      </div>
    </div>
  );
};

export default Home;

