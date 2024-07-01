import React, { useState } from 'react';
import './CSS/PrepareInterview.css'; 
import { useNavigate } from 'react-router-dom';

const PrepareInterview = () => {
  const [showImageForm, setShowImageForm] = useState(false);
  const [showTextForm, setShowTextForm] = useState(false);
  const [jobDescription, setJobDescription] = useState('');

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
    try {
      const response = await fetch(`http://127.0.0.1:8000/prediction/mindmap/?desc=${encodeURIComponent(jobDescription)}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const mindmap = data.code.replace(/```/g, '').replace('mermaid\n', '');

      console.log('Mindmap:', mindmap);

      navigate('/mindmap', { state: { mindmap: mindmap } });
      
      
    } catch (error) {
      console.error('Error fetching the mindmap:', error);
    }
  };

  return (
    <div className="container">
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
    </div>
  );
};

export default PrepareInterview;
