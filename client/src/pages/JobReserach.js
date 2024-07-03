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

        const url = new URL('http://localhost:8000/prediction/job_report');
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
        <div className="container">
            <h2>Job Research</h2>
            {!reportGenerated ? (
                <form>
                    <label>
                        Company:
                        <input
                            type="text"
                            name="job_poster"
                            value={jobPoster}
                            onChange={(e) => setJobPoster(e.target.value)}
                            disabled={loading}  // Disable input when loading
                        />
                    </label>
                    <label>
                        Job Description:
                        <textarea
                            name="desc"
                            value={desc}
                            onChange={(e) => setDesc(e.target.value)}
                            disabled={loading}  // Disable textarea when loading
                        />
                    </label>
                    <button type="button" onClick={handleResearchJob} disabled={loading}>
                        {loading ? 'Generating Report...' : 'Research Job'}  
                    </button>
                </form>
            ) : (
                <div>
                    <h3>Job Report</h3>
                    <ReactMarkdown>{report}</ReactMarkdown>
                    <button type="button" onClick={handleNewSearch}>
                        Search New
                    </button>
                </div>
            )}
            {loading && (
                <div>
                    <p>Loading...</p>
                    <p>This will take some time</p>
                </div>
            )}
        </div>
    );
};

export default JobResearch;
