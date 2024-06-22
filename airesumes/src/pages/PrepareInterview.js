import React, { useState } from 'react';

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
      <div>
        <div onClick={handleImageClick} style={{ cursor: 'pointer', marginBottom: '10px', border: '1px solid black', padding: '10px' }}>
          Upload Image
        </div>
        <div onClick={handleTextClick} style={{ cursor: 'pointer', marginBottom: '10px', border: '1px solid black', padding: '10px' }}>
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
