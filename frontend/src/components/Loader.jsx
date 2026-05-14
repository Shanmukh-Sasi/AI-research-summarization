import React from 'react';

const Loader = ({ message }) => {
  return (
    <div className="loader-container">
      <div className="spinner"></div>
      {message && <p className="loader-message">{message}</p>}
    </div>
  );
};

export default Loader;
