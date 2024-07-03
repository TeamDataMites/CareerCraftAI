import React, { useState } from 'react';
import './CSS/PrepareInterview.css'; 
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
      const response = await fetch(`http://localhost:8000/prediction/mindmap/?desc=${encodeURIComponent(jobDescription)}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const mindmap = data.code.replace(/```/g, '').replace('mermaid\n', '');

      console.log('Mindmap:', mindmap);

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
      
      const response3 = await fetch(`http://localhost:8000/prediction/mindmap/?desc=${data2}`)

      console.log('Data2:', data2);
      console.log('Response3:', response3);

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
    <div className="container">
      {loading ? (
        <div className="loading-screen">
          Loading...
        </div>
      ) : (
        <>
          <h2>Generate Mind Map</h2>
          <br></br>
          <div className="option" onClick={handleImageClick}>
            Upload Image
          </div>
          <div className="option" onClick={handleTextClick}>
            Input Text
          </div>

          {showImageForm && (
            <form>
              <label>
                Upload Job Flyer:
                <input type="file" accept="image/*" />
              </label>
              <button type="button" onClick={handleExtractText}>
                Generate Mindmap
              </button>
            </form>
          )}

          {showTextForm && (
            <form>
              <label>
                Enter Job Description:
                <textarea value={jobDescription} onChange={handleJobDescriptionChange} />
              </label>
              <button type="button" onClick={handleGenerateMindmap}>
                Generate Mindmap
              </button>
            </form>
          )}
        </>
      )}
    </div>
  );
};

export default PrepareInterview;
