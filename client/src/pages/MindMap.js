import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import mermaid from 'mermaid';

const MindMap = () => {
  const location = useLocation();
  const { mindmap } = location.state || {};

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'forest',
      securityLevel: 'loose',
    });

    if (mindmap) {
      mermaid.contentLoaded();
    }
  }, [mindmap]);

  return (
    <div style={{ backgroundColor: '#1E1E1E',padding:'2%'}}>
      <h1 style={{textAlign:'center', color: '#BB86FC'}}>Things You Should Know</h1>
      <div className='mermaid'>{mindmap}</div>
    </div>
  );
};

export default MindMap;
