import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import githubLogo from './images/github-mark-white.svg'; // Adjust the path as necessary
import WebRecorder from './WebRecorder';
import Results from './Results';

function App() {
  const [songs, setSongs] = useState([]);

  // useEffect(() => {
  //   console.log('Backend URL:', process.env.REACT_APP_BACKEND_URL);
  //   fetch(`${process.env.REACT_APP_BACKEND_URL}/songs`, {
  //     mode: 'cors',
  //   })
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setSongs(data);
  //     });
  // }, []);

  const data = [
    { "track": "In the End", "artist": "Linkin Park" },
    { "track": "Yellow", "artist": "Coldplay" },
    { "track": "Ride", "artist": "Twenty One Pilots" },
    { "track": "Fast Car", "artist": "Luke Combs" },
    { "track": "This Girl (Kungs Vs. Cookin' On 3 Burners)", "artist": "Kungs, Cookin' On 3 Burners" },
    { "track": "Hard Times", "artist": "Paramore" },
    { "track": "Electric Feel", "artist": "MGMT" },
    { "track": "Payphone", "artist": "Maroon 5, Wiz Khalifa" },
    { "track": "Tongue Tied", "artist": "GROUPLOVE" },
    { "track": "The Less I Know The Better", "artist": "Tame Impala" },
    { "track": "Little Talks", "artist": "Of Monsters and Men" },
    { "track": "vampire", "artist": "Olivia Rodrigo" },
    { "track": "Starboy", "artist": "The Weeknd, Daft Punk" },
    { "track": "Miss You", "artist": "Oliver Tree, Robin Schulz" },
    { "track": "Pompeii", "artist": "Bastille" },
    { "track": "Blank Space", "artist": "Taylor Swift" },
    { "track": "Watermelon Sugar", "artist": "Harry Styles" },
    { "track": "I'm Good (Blue)", "artist": "David Guetta, Bebe Rexha" },
    { "track": "Cupid - Twin Ver.", "artist": "FIFTY FIFTY" },
    { "track": "Unwritten", "artist": "Natasha Bedingfield" }
  ];
  
  setSongs(data);

  return (
    <Router>
      <div className="app-container">
        <header className="header">
          <div>
            <h2>Powered by DataStax</h2>
          </div>
          <div>
            <a
              href="https://github.com/sribala20/h2s/tree/main"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img src={githubLogo} alt="GitHub Logo" className="github-logo" />
            </a>
          </div>
        </header>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <WebRecorder />
                <div className="songs-header">Songs in AstraDB :</div>
                <div className="songs-gallery">
                  {songs.map((song, index) => (
                    <div key={index} className="song-bubble">
                      <p>
                        {song.track} - {song.artist}
                      </p>
                    </div>
                  ))}
                </div>
              </>
            }
          />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
