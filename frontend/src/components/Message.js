// Message.js
function Message({ text, isUser }) {
  const messageClass = isUser ? 'user-message' : 'bot-message'; // This will assign the right class based on who the sender is

  return (
    <div className={`message ${messageClass}`}>{text}</div> // Apply the conditional class here
  );
}
  
export default Message;