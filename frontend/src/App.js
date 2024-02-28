import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import  NavBar  from "./components/NavBar";
import Banner from "./components/Banner";
import CoPilot from "./components/CoPilot.js";
import StreamlitDashboard from './components/StreamlitDashboard.js';
import { Skills } from "./components/Skills";
import { Projects } from "./components/Projects";
import { Contact } from "./components/Contact";
import { Footer } from "./components/Footer";

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<Banner/>}/>
          <Route path="/co-pilot" element={<CoPilot/>}/>
          <Route path="/dashboard" element={<StreamlitDashboard/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
