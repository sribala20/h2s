import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import githubLogo from './images/github-mark-white.svg'; // Adjust the path as necessary


function App() {
  const [trackInfo, setTrackInfo] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const micButtonRef = useRef(null);
  const playbackRef = useRef(null);

  let canRecord = false;
  let recorder = null;
  let chunks = [];

  useEffect(() => {
    const micButton = micButtonRef.current;
    const playback = playbackRef.current;

    const setupAudio = async () => {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          setupStream(stream);
        } catch (err) {
          console.error(err);
        }
      }
    };

    const setupStream = (stream) => {
      recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/wav; codecs=opus" });
        setAudioBlob(blob);
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;
      };
      canRecord = true;
    };

    const toggleMic = () => {
      if (!canRecord) return;
      if (recorder.state === 'inactive') {
        recorder.start();
        micButton.classList.add("is-recording");
      } else {
        recorder.stop();
        micButton.classList.remove("is-recording");
      }
    };

    micButton.addEventListener('click', toggleMic);
    setupAudio();

    return () => {
      micButton.removeEventListener('click', toggleMic);
    };
  }, [audioBlob]);

  const handleButtonClick = async () => {
    const formData = new FormData();
    formData.append("audioFile", audioBlob, "recording.mp3");

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const jsonData = await response.json();
      setTrackInfo(jsonData);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  console.log("Track Info:", trackInfo);

  return (
    <div className="app-container">
       <header className="header">
        <div>
          <h2>Powered by DataStax</h2>
        </div>
        <div>
          <a href="https://github.com/your-repo-link" target="_blank" rel="noopener noreferrer">
            <img src={githubLogo} alt="GitHub Logo" className="github-logo" />
          </a>
        </div>
      </header>
      <main>
        <h1>Sing, Hum, or Play to find your song</h1>
        <p>Click the mic and hum a clear tune of one of the songs in the Astra DB song collection, or choose one of the example queries.</p>
        <button className="mic-toggle" ref={micButtonRef}>
          <span className="material-icons">mic</span>
        </button>
        <div className="controls-container">
          <audio className="playback" controls ref={playbackRef}></audio>
          <button className="search-button" onClick={handleButtonClick}>Search</button>
        </div>
        {trackInfo && (
          <div className="track-info">
            <img src={trackInfo.album_image} />
            <h3>{`${trackInfo.track} - ${trackInfo.artist}`}</h3>
            <h4>{trackInfo.album}</h4>
            <audio controls src={trackInfo.track_url} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
