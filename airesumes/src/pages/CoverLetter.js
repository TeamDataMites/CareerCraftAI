import React from 'react';

const CoverLetter = () => {
  return (
    <div>
      <h2>Upload Your CV</h2>
      <form>
        <label>
          Upload CV:
          <input type="file" accept=".pdf,.doc,.docx" />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default CoverLetter;
