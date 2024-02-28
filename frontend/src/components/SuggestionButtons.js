// SuggestionButtons.js - Component to render the suggestion buttons.
import React, { useState } from 'react';

function SuggestionButtons({ onSuggestionClick }) {
  const allSuggestions = [
    'How much total amount did BlackRock invest\n in the year 2019?',
    'Tell me something about BlackRock investments in the region of South Asia',
    'Tell me something about the snapdeal Investment of BlackRock',
    'How much total amount did BlackRock invest\n in the year 2019?',
    'What are some of the deals done by Morgan Stanley in the year 2023?',
    'Tell me something about Inrix Inc.'
  ];

  // Function inside the component to get 4 random unique suggestions
  const getRandomSuggestions = () => {
    let result = new Set();
    while(result.size < 4) {
      let randomIndex = Math.floor(Math.random() * allSuggestions.length);
      result.add(allSuggestions[randomIndex]);
    }
    return [...result];
  };

  const [suggestions, setSuggestions] = useState(getRandomSuggestions());

  return (
    <div className="suggestion-buttons">
      {suggestions.map((suggestion, index) => (
        <button key={index} onClick={() => onSuggestionClick(suggestion)}>
          {suggestion}
        </button>
      ))}
    </div>
  );
}

export default SuggestionButtons;
