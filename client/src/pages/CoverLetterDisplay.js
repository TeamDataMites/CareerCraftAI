import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import jsPDF from 'jspdf';
import './CSS/CoverLetterDisplay.css';

const CoverLetterDisplay = () => {
  const location = useLocation();
  const { coverLetter: initialCoverLetter } = location.state || { coverLetter: '' };
  const [coverLetter, setCoverLetter] = useState(initialCoverLetter);

  const handleDownload = () => {
    const doc = new jsPDF();
    const lines = doc.splitTextToSize(coverLetter, 180); 
    doc.setFontSize(12);
    doc.text(lines, 10, 10); 
    doc.save('cover_letter.pdf');
  };

  return (
    <div className="cover-letter-container">
      <h2>Generated Cover Letter</h2>
      <textarea
        value={coverLetter}
        onChange={(e) => setCoverLetter(e.target.value)}
        rows="20"
        cols="80"
        className="cover-letter-textarea"
      />
      <button className="download-button" onClick={handleDownload}>
        Download Cover Letter (PDF)
      </button>
    </div>
  );
};

export default CoverLetterDisplay;
