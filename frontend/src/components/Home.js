// Home.js
import React from 'react';
import './Home.css'; // Assuming you have a CSS file for styling
import analytics_logo from './analytics_logo.png';
import wwd from './wwd.png';


function Home() {
  return (
    <div className="container">
      <div className="row">
        <div className="col text-content">
          <h2>What we do?</h2>
          <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry...</p>
        </div>
        <div className="col media-content">
          <img src="path_to_your_image.jpg" alt="Descriptive Text" />
        </div>
      </div>
      <div className="row">
        <div className="col media-content">
          <img src="path_to_another_image.jpg" alt="Descriptive Text" />
        </div>
        <div className="col text-content">
          <h2>Our Mission</h2>
          <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry...</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
