
import React, { useState } from 'react';
import jsPDF from 'jspdf';
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

      const uploadUrl = 'http://127.0.0.1:8081/prediction/load_direct';
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
    const doc = new jsPDF();
    doc.text(optimization, 10, 10);
    doc.save('optimized_resume.pdf');
  };

  return (
    <div style={styles.container}>
      {loading && <p>Loading...</p>} {/* Show loading message when loading is true */}
      {!loading && optimization && (
        <div style={styles.resultContainer}>
          <h2 style={styles.heading}>Optimization Result:</h2>
          <div style={styles.resultBox} id="optimization-result">
            <ReactMarkdown value={optimization} rows="20" cols="80" style={styles.textarea} />
          </div>
          <button style={styles.button} onClick={handleDownloadPDF}>Download as PDF</button>
          <button style={styles.button} onClick={() => setOptimization('')}>Reset</button>
        </div>
      )}
      {!loading && !optimization && (
        <form onSubmit={handleSubmit} style={styles.form} disabled={loading}> {/* Disable form when loading */}
          <h2 style={styles.heading}>Optimize Your Resume</h2>
          <label style={styles.label}>
            Upload CV:
            <input type="file" accept=".pdf,.doc,.docx" onChange={handleCvChange} style={styles.input} />
          </label>
          <br />
          <label style={styles.label}>
            LinkedIn URL:
            <input type="text" value={linkdinUrl} onChange={handleLinkdinUrlChange} style={styles.input} />
          </label>
          <br />
          <label style={styles.label}>
            GitHub URL:
            <input type="text" value={githubUrl} onChange={handleGithubUrlChange} style={styles.input} />
          </label>
          <br />
          <label style={styles.label}>
            Personal Writeup:
            <input type="text" value={personalWriteup} onChange={handlePersonalWriteupChange} style={styles.input} />
          </label>
          <br />
          <label style={styles.label}>
            Job Post:
            <input type="text" value={jobPost} onChange={handleJobPostChange} style={styles.input} />
          </label>
          <br />
          <button type="submit" style={styles.submitButton} disabled={loading}>Submit</button> {/* Disable submit button when loading */}
        </form>
      )}
    </div>
  );
};

const styles = {
  container: {
    margin: '0 auto',
    backgroundColor: '#1E1E1E', /* Darker blue */
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    fontFamily: 'Arial, sans-serif',
    color: '#FFFFFF', /* White */
    textAlign: 'center',
    paddingTop: '50px',
  },
  resultContainer: {
    backgroundColor: '#1E1E1E', /* Darker blue */
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    marginBottom: '20px',
    textAlign: 'left',
  },
  heading: {
    color: '#BB86FC', /* Light purple */
    marginBottom: '20px',
  },
  resultBox: {
    backgroundColor: '#FFFFFF', /* Dark gray */
    padding: '10px',
    borderRadius: '5px',
    marginBottom: '20px',
    textAlign: 'left',
    color: '#000000', /* Black */
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#BB86FC', /* Light purple */
    color: '#FFFFFF', /* White */
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    marginRight: '10px',
  },
  form: {
    maxWidth: '600px',
    textAlign: 'center',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    marginLeft: '30%',
    marginBottom: '90px',
  },
  label: {
    display: 'block',
    marginBottom: '10px',
    color: '#FFFFFF', /* White */
  },
  input: {
    padding: '8px',
    borderRadius: '5px',
    border: '1px solid #BB86FC', /* Light purple */
    marginBottom: '10px',
    width: '100%',
    boxSizing: 'border-box',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#BB86FC', /* Light purple */
    color: '#FFFFFF', /* White */
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
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
};

export default ResumeBuild;
