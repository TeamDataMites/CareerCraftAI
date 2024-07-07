import React from 'react';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';
import Home from './pages/Home';
import ResumeBuild from './pages/ResumeBuild';
import CoverLetter from './pages/CoverLetter';
import PrepareInterview from './pages/PrepareInterview';
import CoverLetterDisplay from './pages/CoverLetterDisplay';
import Login from './pages/Log';
import MindMap from './pages/MindMap';
import JobResearch from './pages/JobReserach';
import LectureNone from './pages/LectureNone';
import Assistant from './pages/VoiceAssistant';

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
        <Route path="/lecture-note" element={<LectureNone />} />
        <Route path="/help-desk" element={<Assistant/>} />
      </Routes>
    </Router>
  );
};

export default App;
