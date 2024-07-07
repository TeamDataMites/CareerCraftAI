import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import jsPDF from 'jspdf';

const LectureNone = () => {
    const [topic, setTopic] = useState('');
    const [domain, setDomain] = useState('');
    const [lectureNote, setLectureNote] = useState('');
    const lectureNoteRef = useRef(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const url = `http://127.0.0.1:8081/prediction/lecture_note/?topic=${topic}&domain=${domain}`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();
            console.log(data);
            setLectureNote(data.note);
        } catch (error) {
            console.error('Error fetching lecture note:', error);
        }
    };

    const handleDownloadPDF = () => {
        const doc = new jsPDF();
        doc.setFontSize(12);
        doc.text(lectureNoteRef.current.textContent, 10, 10);
        doc.save('lecture-note.pdf');
    };

    const handleReload = () => {
        window.location.reload();
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Generated Lecture Note</h2>
            {!lectureNote ? (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>Topic:</label> <br />
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            style={styles.textarea}
                        />
                    </div>
                    <div>
                        <label>Domain:</label> <br />
                        <input
                            type="text"
                            value={domain}
                            onChange={(e) => setDomain(e.target.value)}
                            style={styles.textarea}
                        />
                    </div>
                    <button type="submit" style={styles.button}>Submit</button>
                </form>
            ) : (
                <div>
                    <div ref={lectureNoteRef} style={styles.lectureNote}>
                        <ReactMarkdown>{lectureNote}</ReactMarkdown>
                    </div>
                    <button onClick={handleDownloadPDF} style={styles.button}>Download as PDF</button>
                    <button onClick={handleReload} style={styles.button}>Reload</button>
                </div>
            )}
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
        width: '600px',
    },
    button: {
        padding: '10px 20px',
        borderRadius: '4px',
        border: 'none',
        backgroundColor: '#BB86FC', // Light purple
        color: '#FFFFFF', // White
        cursor: 'pointer',
        width: '150px',
        margin: '10px', // Adjust margin
    },
    lectureNote: {
        backgroundColor: '#1E1E1E', // Darker blue
        color: '#FFFFFF', // White
        padding: '10px',
        borderRadius: '8px',
        border: 'none',
        width: '80%',
        maxWidth: '600px',
        marginTop: '20px',
        whiteSpace: 'pre-wrap', // Preserve whitespace and newlines
    },
};

export default LectureNone;
