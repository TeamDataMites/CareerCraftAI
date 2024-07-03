import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const JobResearch = () => {
    const [jobPoster, setJobPoster] = useState('');
    const [desc, setDesc] = useState('');
    const [report, setReport] = useState('');
    const [loading, setLoading] = useState(false);
    const [reportGenerated, setReportGenerated] = useState(false);

    const handleResearchJob = () => {
        setLoading(true);  // Set loading to true when API call starts
        const url = new URL('http://localhost:8000/prediction/job_report');
        url.searchParams.append('job_poster', jobPoster);
        url.searchParams.append('desc', desc);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                setReport(data.report);  // Set the report state with the fetched data
                setLoading(false);  // Set loading to false when API call finishes
                setReportGenerated(true);  // Set reportGenerated to true when report is generated
            })
            .catch(error => {
                console.error('Error fetching job report:', error);
                setLoading(false);  // Set loading to false if API call fails
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
