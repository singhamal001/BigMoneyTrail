import React, { useState } from 'react';
import '@fontsource/roboto';
import Greeting from './Greeting';
import SuggestionButtons from './SuggestionButtons';
import ChatBox from './ChatBox';
import Response from './Response';
import Message from './Message';

function CoPilot() {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([])
  const [showSuggestionButtons, setShowSuggestionButtons] = useState(true);

  
  // Function to handle when a suggestion button is clicked
  const handleSuggestionClick = async (suggestion) => {
    // You would send this suggestion to the backend
    console.log('Suggestion sent to the backend:', suggestion);
    setMessages(prevMessages => [...prevMessages, { text: suggestion, isUser: true }]);
    const response = await fetch('http://localhost:5000/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: suggestion }),
    });

    if (response.ok) {
      setShowSuggestionButtons(false); 
      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages,{ text: <Response text={data.response} />, isUser: false },]);
      console.log('Response from the backend:', data);
    } else {
      console.error('Error sending suggestion to the backend:', response.statusText);
    }
  };
  
  const updateUserInput = (newInput) => {
    setUserInput(newInput);
  };

  // Function to handle when the user sends a message through the chatbox
  const handleMessageSubmit = async(input) => {
    console.log('User input sent to the backend:', input);
    setMessages((prevMessages) => [...prevMessages, { text: input, isUser: true }]);
    setUserInput(''); // Reset the userInput to an empty string

    const response = await fetch('http://localhost:5000/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: input }),
    });

    if (response.ok) {
      setShowSuggestionButtons(false); 
      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages,{ text: <Response text={data.response} />, isUser: false },]);
      console.log('Response from the backend:', data);
    } else {
      console.error('Error sending user input to the backend:', response.statusText);
    }
  };

  return (
    <div className="CoPilot">
      <div className="Greeting">
        <Greeting />
      </div>
      {showSuggestionButtons && <SuggestionButtons onSuggestionClick={handleSuggestionClick} />}
      {/* <MessagesDisplay messages={messages} /> */}
      <ChatBox userInput={userInput} onUpdateUserInput={updateUserInput} onMessageSubmit={handleMessageSubmit} />
      <div className="messages-container" style={{ overflow: 'auto', height: '400px' }}>
        {messages.map((message, index) => (
          <Message key={index} text={message.text} isUser={message.isUser} />
        ))}
      </div>
    </div>
  );
}

export default CoPilot;