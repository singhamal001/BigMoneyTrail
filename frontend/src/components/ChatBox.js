// ChatBox.js - Component for the chatbox.

import React from 'react';

function ChatBox({ userInput, onUpdateUserInput, onMessageSubmit }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onMessageSubmit(userInput);
  };

  return (
    <form className="chatbox" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Ask your questions"
        value={userInput}
        onChange={(e) => onUpdateUserInput(e.target.value)}
        disabled={false}
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default ChatBox;
