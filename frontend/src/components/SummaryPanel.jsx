import React from 'react';
import { BookOpen } from 'lucide-react';

const SummaryPanel = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="summary-panel card animate-fade-in">
      <div className="panel-header">
        <BookOpen size={24} />
        <h2>Document Summary</h2>
      </div>
      <div className="summary-content">
        <p>{typeof summary === 'string' ? summary : JSON.stringify(summary)}</p>
      </div>
    </div>
  );
};

export default SummaryPanel;
