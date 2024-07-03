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
        body: formData
      });
  
      if (!response.ok) {
        throw new Error('Failed to upload file');
      }
  
      const responseData = await response.json();

      const query = responseData.extratedtext;

      const send_data = {"query":query, "jobposition":e.target.jobposition.value}

      const uploadUrl2 = 'http://localhost:8081/generate_cover_letter';

      const response2 = await fetch(uploadUrl2, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(send_data)
      });

      if (!response2.ok) {
        throw new Error('Failed to upload file');
      }

      const responseData2 = await response2.json();
      navigate('/cover-letter', { state: { coverLetter: responseData2.cover_letter } });
      
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h2>Upload Your CV</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Upload CV:
          <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
        </label>
        <label>
          Input Job Role:
          <input type="text" name="jobposition" />
        </label>

        <button type="submit" disabled={loading}>Submit</button>
      </form>
      
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      
      {extractedText && (
        <div>
          <h3>Extracted Text:</h3>
          <p>{extractedText}</p>
        </div>
      )}
    </div>
  );
};

export default CoverLetter;

