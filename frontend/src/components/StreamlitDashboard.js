import React from 'react';

function StreamlitDashboard() {
  const streamlitURL = "http://localhost:8501/"; // Replace with your Streamlit URL

  return (
    <div className="streamlit-dashboard" style={{width: '100%', height: '100vh'}}>
      <iframe
        src={streamlitURL}
        title="Streamlit Dashboard"
        style={{
          border: 'none',
          width: '100%',
          height: '100%',
        }}
      />
    </div>
  );
}

export default StreamlitDashboard;
