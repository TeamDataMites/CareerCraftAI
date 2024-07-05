import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import jsPDF from 'jspdf';
import './CSS/CoverLetterDisplay.css'; // Assuming you have specific styles for this component

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
    <div className="cover-letter-container" style={styles.container}>
      <h2 style={styles.header}>Generated Cover Letter</h2>
      <textarea
        value={coverLetter}
        onChange={(e) => setCoverLetter(e.target.value)}
        rows="20"
        cols="80"
        className="cover-letter-textarea"
        style={styles.textarea}
      />
      <button className="download-button" onClick={handleDownload} style={styles.button}>
        Download Cover Letter (PDF)
      </button>
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
  textarea: {
    backgroundColor: '#1E1E1E', // Darker blue
    color: '#FFFFFF', // White
    padding: '10px',
    borderRadius: '8px',
    border: 'none',
    resize: 'vertical',
    minHeight: '400px',
    maxWidth: '100%',
    minWidth: '80%',
    marginBottom: '20px',
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

export default CoverLetterDisplay;
