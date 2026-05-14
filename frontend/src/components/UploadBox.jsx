import React, { useState } from 'react';
import { Upload, FileText, CheckCircle } from 'lucide-react';

const UploadBox = ({ onUpload, isLoading }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    } else {
      alert('Please select a valid PDF file.');
    }
  };

  const handleUpload = () => {
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="upload-box card">
      <div className="upload-header">
        <Upload size={24} />
        <h2>Upload Research Paper</h2>
      </div>
      
      <div className={`drop-zone ${file ? 'has-file' : ''}`}>
        <input 
          type="file" 
          id="pdf-upload" 
          accept=".pdf" 
          onChange={handleFileChange} 
          hidden 
        />
        <label htmlFor="pdf-upload" className="drop-zone-content">
          {file ? (
            <div className="file-info">
              <FileText size={48} className="file-icon" />
              <p className="file-name">{file.name}</p>
              <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          ) : (
            <div className="upload-placeholder">
              <Upload size={48} className="upload-icon" />
              <p>Click or drag PDF here</p>
            </div>
          )}
        </label>
      </div>

      <button 
        className="btn btn-primary btn-block" 
        onClick={handleUpload} 
        disabled={!file || isLoading}
      >
        {isLoading ? 'Processing...' : 'Upload & Summarize'}
      </button>
    </div>
  );
};

export default UploadBox;
