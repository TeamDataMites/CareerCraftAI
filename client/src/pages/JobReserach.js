import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const JobResearch = () => {
    const [jobPoster, setJobPoster] = useState('');
    const [desc, setDesc] = useState('');
    const [report, setReport] = useState('');
    const [loading, setLoading] = useState(false);
    const [reportGenerated, setReportGenerated] = useState(false);

    const handleResearchJob = () => {
        setLoading(true);  

        const url = new URL('http://127.0.0.1:8081/prediction/job_report');
        url.searchParams.append('job_poster', jobPoster);
        url.searchParams.append('desc', desc);
    
        const url2 = 'http://localhost:8082/server/saveinmongo';
        const requestbody = {
            username : sessionStorage.getItem('username'),
            desc: desc
        };
    
        fetch(url2, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestbody)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data saved in MongoDB:', data);
            return fetch(url);
        })
        .then(response => response.json())
        .then(data => {
            setReport(data.report);  
            setLoading(false);  
            setReportGenerated(true);  
        })
        .catch(error => {
            console.error('Error handling research job:', error);
            setLoading(false); 
        });
    };
    

    const handleNewSearch = () => {
        setJobPoster('');
        setDesc('');
        setReport('');
        setReportGenerated(false);
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.heading}>Job Research</h2>
            {!reportGenerated ? (
                <form style={styles.form}>
                    <label style={styles.label}>
                        Company:
                        <input
                            type="text"
                            name="job_poster"
                            value={jobPoster}
                            onChange={(e) => setJobPoster(e.target.value)}
                            disabled={loading}  // Disable input when loading
                            style={styles.input}
                        />
                    </label>
                    <label style={styles.label}>
                        Job Description:
                        <textarea
                            name="desc"
                            value={desc}
                            onChange={(e) => setDesc(e.target.value)}
                            disabled={loading}  // Disable textarea when loading
                            style={styles.input}
                        />
                    </label>
                    <button type="button" onClick={handleResearchJob} disabled={loading} style={styles.submitButton}>
                        {loading ? 'Generating Report...' : 'Research Job'}  
                    </button>
                </form>
            ) : (
                <div style={{...styles.resultContainer, width: '90%'}}>
                    <h3 style={styles.heading}>Job Report</h3>
                    <div style={styles.resultBox}>
                        <ReactMarkdown>{report}</ReactMarkdown>
                    </div>
                    <button type="button" onClick={handleNewSearch} style={styles.button}>
                        Search New
                    </button>
                </div>
            )}
            {loading && (
                <div style={styles.loadingContainer}>
                    <p>Loading...</p>
                    <p>This will take some time</p>
                </div>
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
        height : '100vh',
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
        backgroundColor: '#2E2E2E', /* Dark gray */
        padding: '10px',
        borderRadius: '5px',
        marginBottom: '20px',
        textAlign: 'left',
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
    label: {
        display: 'block',
        marginBottom: '10px',
        color: '#FFFFFF', /* White */
        marginBottom: '20px',
    },
    input: {
        padding: '8px',
        borderRadius: '5px',
        border: '1px solid #BB86FC', /* Light purple */
        marginBottom: '10px',
        width: '100%',
        boxSizing: 'border-box',
        marginTop: '10px',
    },
    submitButton: {
        padding: '10px 20px',
        backgroundColor: '#BB86FC', /* Light purple */
        color: '#FFFFFF', /* White */
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        marginTop: '20px',
        width : '200px',
        marginLeft : '32%'
    },
    loadingContainer: {
        backgroundColor: '#1E1E1E', /* Darker blue */
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        marginTop: '20px',
    },

    form : {
        maxWidth: '600px',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        marginLeft: '30%',
        marginBottom: '90px',
    },
};

export default JobResearch;
