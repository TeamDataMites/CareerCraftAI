import React, { useState } from 'react';
import './CSS/ResumeBuild.css';

const ResumeBuild = () => {
  const [cv, setCv] = useState(null);
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [text3, setText3] = useState('');

  const handleCvChange = (event) => {
    setCv(event.target.files[0]);
  };

  const handleText1Change = (event) => {
    setText1(event.target.value);
  };

  const handleText2Change = (event) => {
    setText2(event.target.value);
  };

  const handleText3Change = (event) => {
    setText3(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission
    console.log('CV:', cv);
    console.log('Text Box 1:', text1);
    console.log('Text Box 2:', text2);
    console.log('Text Box 3:', text3);
  };

  return (
    <div>
      <h2>Optimize Your Resume</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Upload CV:
          <input type="file" accept=".pdf,.doc,.docx" onChange={handleCvChange} />
        </label>
        <br />
        <label>
          Text Box 1:
          <input type="text" value={text1} onChange={handleText1Change} />
        </label>
        <br />
        <label>
          Text Box 2:
          <input type="text" value={text2} onChange={handleText2Change} />
        </label>
        <br />
        <label>
          Text Box 3:
          <input type="text" value={text3} onChange={handleText3Change} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ResumeBuild;
