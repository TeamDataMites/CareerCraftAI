import React from "react";

const JobResearch = () => {
    return (
        <div className="container">
        <h2>Job Research</h2>
        
        <form>
        <label>
            Company:
          <input type="text" name="company" />
        </label>
        <label>
            Job Description:
          <textarea type="text" name="jobdescription" />
        </label>
        <button type="button">
            Research Job
        </button>
        </form>
        </div>
    );
    }

export default JobResearch;