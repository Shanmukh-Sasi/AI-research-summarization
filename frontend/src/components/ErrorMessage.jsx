import React from 'react';
import { AlertCircle } from 'lucide-react';

const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div className="error-container">
      <AlertCircle size={20} />
      <span>{message}</span>
    </div>
  );
};

export default ErrorMessage;
