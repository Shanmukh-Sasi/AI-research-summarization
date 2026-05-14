import React, { useState } from 'react';
import api from './services/api';
import UploadBox from './components/UploadBox';
import SummaryPanel from './components/SummaryPanel';
import ChatBox from './components/ChatBox';
import Loader from './components/Loader';
import ErrorMessage from './components/ErrorMessage';
import './App.css';

function App() {
  const [docId, setDocId] = useState(null);
  const [summary, setSummary] = useState('');
  const [history, setHistory] = useState([]);
  const [documentList, setDocumentList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchDocuments = async () => {
    try {
      const response = await api.getDocuments();
      setDocumentList(response.data);
    } catch (err) {
      console.error("Failed to fetch document list:", err);
    }
  };

  const loadDocument = async (doc) => {
    setIsLoading(true);
    setError('');
    setDocId(doc.id);
    try {
      const response = await api.getDocument(doc.id);
      setSummary(response.data.summary);
      fetchHistory(doc.id);
    } catch (err) {
      setError("Failed to load document details.");
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchHistory = async (id) => {
    try {
      const response = await api.getHistory(id);
      setHistory(response.data.reverse());
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  const handleUpload = async (file) => {
    setIsLoading(true);
    setError('');
    try {
      const response = await api.uploadFile(file);
      const newDocId = response.data.document_id;
      setDocId(newDocId);
      setSummary(response.data.summary);
      setHistory([]);
      fetchDocuments(); // Refresh list after upload
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload and process document.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAsk = async (question) => {
    if (!docId) return;
    setIsLoading(true);
    setError('');
    try {
      const response = await api.askQuestion(docId, question);
      // Update history locally for immediate UI feedback
      setHistory(prev => [...prev, { question, answer: response.data.answer }]);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get an answer.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>AI Research Paper <span>Assistant</span></h1>
          <p>Extract insights from complex papers instantly</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="grid">
            <div className="sidebar">
              <UploadBox onUpload={handleUpload} isLoading={isLoading} />
              <ErrorMessage message={error} />
              
              <div className="history-list card">
                <div className="panel-header">
                  <h3>Previous Documents</h3>
                </div>
                <div className="doc-items">
                  {documentList.length === 0 ? (
                    <p className="empty-msg">No uploads yet</p>
                  ) : (
                    documentList.map(doc => (
                      <div 
                        key={doc.id} 
                        className={`doc-item ${docId === doc.id ? 'active' : ''}`}
                        onClick={() => loadDocument(doc)}
                      >
                        <span className="doc-name">{doc.filename}</span>
                        <span className="doc-date">{new Date(doc.uploaded_at).toLocaleDateString()}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {isLoading && !docId && <Loader message="Extracting text and generating summary..." />}
            </div>

            <div className="content-area">
              {!docId ? (
                <div className="welcome-card card">
                  <h2>Welcome!</h2>
                  <p>Upload a research paper in PDF format to get started. Our AI will summarize it for you and answer your questions based on its content.</p>
                </div>
              ) : (
                <>
                  <SummaryPanel summary={summary} />
                  <ChatBox onAsk={handleAsk} history={history} isLoading={isLoading} />
                </>
              )}
            </div>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 AI Research Paper Summarization System</p>
      </footer>
    </div>
  );
}

export default App;
