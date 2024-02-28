// MessagesDisplay.js
import React from 'react';

const MessagesDisplay = ({ messages }) => {
  return (
    <div className="messages-display">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.author}`}>
          {message.text}
        </div>
      ))}
    </div>
  );
};

export default MessagesDisplay;