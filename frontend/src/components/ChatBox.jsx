import React, { useState, useEffect, useRef } from 'react';
import { Send, MessageSquare } from 'lucide-react';

const ChatBox = ({ onAsk, history, isLoading }) => {
  const [question, setQuestion] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onAsk(question);
      setQuestion('');
    }
  };

  return (
    <div className="chat-box card animate-fade-in">
      <div className="panel-header">
        <MessageSquare size={24} />
        <h2>Ask the Document</h2>
      </div>

      <div className="chat-messages">
        {history.length === 0 ? (
          <div className="empty-chat">
            <p>No questions yet. Ask something about the paper!</p>
          </div>
        ) : (
          history.map((item, index) => (
            <div key={index} className="chat-pair">
              <div className="message user-message">
                <div className="message-label">Q:</div>
                <div className="message-text">{item.question}</div>
              </div>
              <div className="message bot-message">
                <div className="message-label">A:</div>
                <div className="message-text">{item.answer}</div>
              </div>
            </div>
          ))
        )}
        <div ref={chatEndRef} />
      </div>

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" disabled={!question.trim() || isLoading}>
          {isLoading ? <div className="btn-spinner"></div> : <Send size={20} />}
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
