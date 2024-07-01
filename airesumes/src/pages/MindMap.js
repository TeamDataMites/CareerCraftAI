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
    <div>
      <h1>Mind Map</h1>
      <div className='mermaid'>{mindmap}</div>
    </div>
  );
};

export default MindMap;
