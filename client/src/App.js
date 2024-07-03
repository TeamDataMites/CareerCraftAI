import React from 'react';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';
import Home from './pages/Home';
import ResumeBuild from './pages/ResumeBuild';
import CoverLetter from './pages/CoverLetter';
import PrepareInterview from './pages/PrepareInterview';
import CoverLetterDisplay from './pages/CoverLetterDisplay';
import Login from './pages/Login';
import MindMap from './pages/MindMap';
import JobResearch from './pages/JobReserach';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/build-resume" element={<ResumeBuild />} />
        <Route path="/build-cover-letter" element={<CoverLetter />} />
        <Route path="/prepare-interview" element={<PrepareInterview />} />
        <Route path="/cover-letter" element={<CoverLetterDisplay />} />
        <Route path="/mindmap" element={<MindMap />} />
        <Route path="/job-research" element={<JobResearch/>} />
      </Routes>
    </Router>
  );
};

export default App;
