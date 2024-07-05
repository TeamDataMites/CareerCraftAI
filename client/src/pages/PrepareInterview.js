import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PrepareInterview = () => {
  const [showImageForm, setShowImageForm] = useState(false);
  const [showTextForm, setShowTextForm] = useState(false);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleImageClick = () => {
    setShowImageForm(true);
    setShowTextForm(false);
  };

  const handleTextClick = () => {
    setShowTextForm(true);
    setShowImageForm(false);
  };

  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);
  };

  const handleGenerateMindmap = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8081/prediction/mindmap/?desc=${encodeURIComponent(jobDescription)}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const mindmap = data.code.replace(/```/g, '').replace('mermaid\n', '');

      navigate('/mindmap', { state: { mindmap: mindmap } });
      
    } catch (error) {
      console.error('Error fetching the mindmap:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractText = async () => {
    setLoading(true);
    const fileInput = document.querySelector('input[type="file"]');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
      const response = await fetch('http://localhost:5000/uploader', { method: 'POST', body: formData });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const request_data = JSON.stringify({ extract_text: data.text });

      const response2 = await fetch('http://localhost:8082/server/ocrtextcontext', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: request_data
      });
      
      if (!response2.ok) {
        throw new Error('Network response was not ok');
      }
      const data2 = await response2.json();
      
      const response3 = await fetch(`http://127.0.0.1:8081/prediction/mindmap/?desc=${data2}`)

      if (!response3.ok) {
        throw new Error('Network response was not ok');
      }
      const data3 = await response3.json();
      const mindmap = data3.code.replace(/```/g, '').replace('mermaid\n', '');

      navigate('/mindmap', { state: { mindmap: mindmap } });

    } catch (error) {
      console.error('Error extracting text:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container" style={styles.container}>
      {loading ? (
        <div className="loading-screen" style={styles.loadingScreen}>
          Loading...
        </div>
      ) : (
        <>
          <h2 style={styles.header}>Generate Mind Map</h2>
          <br />
          <div className="option" style={styles.option} onClick={handleImageClick}>
            Upload Image
          </div>
          <div className="option" style={styles.option} onClick={handleTextClick}>
            Input Text
          </div>

          {showImageForm && (
            <form>
              <label style={styles.label}>
                Upload Job Flyer:
                <input type="file" accept="image/*" />
              </label>
              <button type="button" onClick={handleExtractText} style={styles.button}>
                Generate Mindmap
              </button>
            </form>
          )}

          {showTextForm && (
            <form>
              <label style={styles.label}>
                Enter Job Description:
                <textarea value={jobDescription} onChange={handleJobDescriptionChange} style={styles.textarea} />
              </label>
              <button type="button" onClick={handleGenerateMindmap} style={styles.button}>
                Generate Mindmap
              </button>
            </form>
          )}
        </>
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
  loadingScreen: {
    color: '#FFFFFF', // White
  },
  header: {
    marginBottom: '20px',
    color: '#BB86FC', // Light purple
  },
  option: {
    backgroundColor: '#1E1E1E', // Darker blue
    color: '#FFFFFF', // White
    padding: '10px',
    margin: '5px',
    borderRadius: '5px',
    cursor: 'pointer',
    width: '150px',
    textAlign: 'center',
  },
  label: {
    marginBottom: '10px',
    color: '#FFFFFF', // White
  },
  textarea: {
    backgroundColor: '#2E2E2E', // Dark gray
    color: '#FFFFFF', // White
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #BB86FC', // Light purple
    width: '100%',
    minHeight: '150px',
    resize: 'vertical',
  },
  button: {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#BB86FC', // Light purple
    color: '#FFFFFF', // White
    cursor: 'pointer',
    marginTop: '10px',
  },
};

export default PrepareInterview;
