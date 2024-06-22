import React from 'react';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';
import Home from './pages/Home';
import ResumeBuild from './pages/ResumeBuild';
import CoverLetter from './pages/CoverLetter';
import PrepareInterview from './pages/PrepareInterview';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/build-resume" element={<ResumeBuild />} />
        <Route path="/build-cover-letter" element={<CoverLetter />} />
        <Route path="/prepare-interview" element={<PrepareInterview />} />
      </Routes>
    </Router>
  );
};

export default App;
