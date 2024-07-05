import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const CoverLetter = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading] = useState(false);
  const [extractedText] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setErrorMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    const uploadUrl = 'http://localhost:8080/extract-text';

    try {
      const response = await fetch(uploadUrl, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const responseData = await response.json();

      const query = responseData.extratedtext;

      const send_data = { query: query, jobposition: e.target.jobposition.value };

      const uploadUrl2 = 'http://localhost:8081/generate_cover_letter';

      const response2 = await fetch(uploadUrl2, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(send_data),
      });

      if (!response2.ok) {
        throw new Error('Failed to generate cover letter');
      }

      const responseData2 = await response2.json();
      navigate('/cover-letter', { state: { coverLetter: responseData2.cover_letter } });

    } catch (error) {
      console.error('Error handling cover letter:', error);
    }
  };

  return (
    <div style={styles.container}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <h2 style={styles.header}>Build The Cover Letter</h2>
        <label style={styles.label}>
          Upload CV:
          <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} style={styles.input} />
        </label>
        <label style={styles.label}>
          Input Job Role:
          <input type="text" name="jobposition" style={styles.input} />
        </label>

        <button type="submit" disabled={loading} style={styles.button}>
          Submit
        </button>
      </form>

      {errorMessage && <p style={styles.error}>{errorMessage}</p>}

      {extractedText && (
        <div style={styles.extractedText}>
          <h3 style={styles.header}>Extracted Text:</h3>
          <p>{extractedText}</p>
        </div>
      )}
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
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: '#1E1E1E', // Darker blue
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    width: '80%',
    maxWidth: '600px',
  },
  header: {
    marginBottom: '20px',
    color: '#BB86FC', // Light purple
  },
  label: {
    marginBottom: '10px',
    color: '#BB86FC', // Light purple
    width: '100%',
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
    width: '50%',
  },
  error: {
    color: 'red',
    marginTop: '10px',
  },
  extractedText: {
    marginTop: '20px',
    textAlign: 'left',
    width: '80%',
    maxWidth: '600px',
  },
};

export default CoverLetter;
