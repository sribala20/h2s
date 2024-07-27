import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import "./App.css";
import githubLogo from "./images/github-mark-white.svg"; // Adjust the path as necessary
import WebRecorder from "./WebRecorder";
import Results from "./Results";

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="header">
          <div>
            <h2>Powered by DataStax</h2>
          </div>
          <div>
            <a
              href="https://github.com/your-repo-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img src={githubLogo} alt="GitHub Logo" className="github-logo" />
            </a>
          </div>
        </header>
        <Routes>
          <Route path="/" element={<WebRecorder />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
