import React, { useState } from 'react';

const LectureNone = () => {
    const [topic, setTopic] = useState('');
    const [domain, setDomain] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const url = `http://127.0.0.1:8081/prediction/lecture_note/?topic=${topic}&domain=${domain}`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();
            console.log(data); // Handle the response data as needed
        } catch (error) {
            console.error('Error fetching lecture note:', error);
        }
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Generated Lecture Note</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Topic:
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            style={styles.textarea}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Domain:
                        <input
                            type="text"
                            value={domain}
                            onChange={(e) => setDomain(e.target.value)}
                            style={styles.textarea}
                        />
                    </label>
                </div>
                <button type="submit" style={styles.button}>Submit</button>
            </form>
        </div>
    );
};

const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#121212', // Dark blue
      color: '#FFFFFF', // White
    },
    header: {
      marginBottom: '20px',
      color: '#BB86FC', // Light purple
    },
    textarea: {
      backgroundColor: '#1E1E1E', // Darker blue
      color: '#FFFFFF', // White
      padding: '10px',
      borderRadius: '8px',
      border: 'none',
      resize: 'vertical',
      minHeight: '40px',
      maxWidth: '100%',
      minWidth: '80%',
      marginBottom: '20px',
      width:'600px'
    },
    button: {
      padding: '10px 20px',
      borderRadius: '4px',
      border: 'none',
      backgroundColor: '#BB86FC', // Light purple
      color: '#FFFFFF', // White
      cursor: 'pointer',
      width:'150px',
      marginLeft:'250px'
    },
};

export default LectureNone;
