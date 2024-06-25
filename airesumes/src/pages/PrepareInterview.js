import React, { useState } from 'react';
import './CSS/PrepareInterview.css'; // Import the CSS file

const PrepareInterview = () => {
  const [showImageForm, setShowImageForm] = useState(false);
  const [showTextForm, setShowTextForm] = useState(false);

  const handleImageClick = () => {
    setShowImageForm(true);
    setShowTextForm(false);
  };

  const handleTextClick = () => {
    setShowTextForm(true);
    setShowImageForm(false);
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
            <textarea type="text" />
          </label>
        </form>
      )}
    </div>
  );
};

export default PrepareInterview;
