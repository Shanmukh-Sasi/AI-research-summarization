import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = {
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  askQuestion: (documentId, question) => {
    return axios.post(`${API_BASE_URL}/ask`, {
      document_id: documentId,
      question: question,
    });
  },

  getHistory: (documentId) => {
    return axios.get(`${API_BASE_URL}/history/${documentId}`);
  },

  getDocuments: () => {
    return axios.get(`${API_BASE_URL}/documents`);
  },

  getDocument: (documentId) => {
    return axios.get(`${API_BASE_URL}/document/${documentId}`);
  },
};

export default api;
