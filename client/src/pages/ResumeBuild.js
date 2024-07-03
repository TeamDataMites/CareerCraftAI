import React, { useState } from 'react';
import './CSS/ResumeBuild.css';
import ReactMarkdown from 'react-markdown';

const ResumeBuild = () => {
  const [cv, setCv] = useState(null);
  const [linkdinUrl, setLinkdinUrl] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [personalWriteup, setPersonalWriteup] = useState('');
  const [jobPost, setJobPost] = useState('');
  const [resume, setResume] = useState('');
  const [loading, setLoading] = useState(false); 
  const [optimization, setOptimization] = useState('');

  const handleCvChange = (event) => {
    setCv(event.target.files[0]);
  };

  const handleLinkdinUrlChange = (event) => {
    setLinkdinUrl(event.target.value);
  };

  const handleGithubUrlChange = (event) => {
    setGithubUrl(event.target.value);
  };

  const handlePersonalWriteupChange = (event) => {
    setPersonalWriteup(event.target.value);
  };

  const handleJobPostChange = (event) => {
    setJobPost(event.target.value);
  };

  const generateRandomTaskName = () => {
    return 'task_' + Math.random().toString(36).substr(2, 9);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true when form is submitted

    try {
      const taskName = generateRandomTaskName();
      const formData = new FormData();
      formData.append('task_name', taskName);
      formData.append('linkdin_url', linkdinUrl);
      formData.append('github_url', githubUrl);
      formData.append('personal_writeup', personalWriteup);
      formData.append('job_post', jobPost);
      formData.append('file', cv);

      const response = await fetch('http://localhost:8080/extract-text', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      setResume(responseData.extratedtext);

      const uploadUrl = 'http://localhost:8000/prediction/load_direct';
      const response2 = await fetch(uploadUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_name: taskName,
          linkdin_url: linkdinUrl,
          github_url: githubUrl,
          personal_writeup: personalWriteup,
          job_post: jobPost,
          resume: responseData.extratedtext,
        }),
      });

      if (!response2.ok) {
        throw new Error('Failed to upload file');
      }

      const responseData2 = await response2.json();
      setOptimization(responseData2.result);

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false); // Reset loading after request completes
    }
  };

  const handleDownloadPDF = () => {
    // Create a new iframe element
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);

    // Set iframe content with the Markdown content to print
    const content = `<html><body>${optimization}</body></html>`;
    const doc = iframe.contentWindow.document;
    doc.open();
    doc.write(content);
    doc.close();

    // Print the iframe content
    iframe.contentWindow.focus();
    iframe.contentWindow.print();

    // Remove the iframe from the DOM
    document.body.removeChild(iframe);
  };

  return (
    <div>
      {loading && <p>Loading...</p>} {/* Show loading message when loading is true */}
      {!loading && optimization && (
        <div>
          <h2>Optimization Result:</h2>
          <div style={{ margin: '10px', border: '1px solid #ccc', padding: '10px' }}>
            <ReactMarkdown>{optimization}</ReactMarkdown>
          </div>
          <button onClick={handleDownloadPDF}>Download as PDF</button>
          <button onClick={() => setOptimization('')}>Reset</button>
        </div>
      )}
      {!loading && !optimization && (
        <form onSubmit={handleSubmit} disabled={loading}> {/* Disable form when loading */}
          <h2>Optimize Your Resume</h2>
          <label>
            Upload CV:
            <input type="file" accept=".pdf,.doc,.docx" onChange={handleCvChange} />
          </label>
          <br />
          <label>
            LinkedIn URL:
            <input type="text" value={linkdinUrl} onChange={handleLinkdinUrlChange} />
          </label>
          <br />
          <label>
            GitHub URL:
            <input type="text" value={githubUrl} onChange={handleGithubUrlChange} />
          </label>
          <br />
          <label>
            Personal Writeup:
            <input type="text" value={personalWriteup} onChange={handlePersonalWriteupChange} />
          </label>
          <br />
          <label>
            Job Post:
            <input type="text" value={jobPost} onChange={handleJobPostChange} />
          </label>
          <br />
          <button type="submit" disabled={loading}>Submit</button> {/* Disable submit button when loading */}
        </form>
      )}
    </div>
  );
};

export default ResumeBuild;
