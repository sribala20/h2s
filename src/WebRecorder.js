import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const [searchText, setSearchText] = useState('Search');
  const [isClicked, setIsClicked] = useState(false);
  const [trackInfo, setTrackInfo] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const micButtonRef = useRef(null);
  const playbackRef = useRef(null);
  const navigate = useNavigate();

  let canRecord = false;
  let recorder = null;
  let chunks = [];

  useEffect(() => {
    const micButton = micButtonRef.current;
    const playback = playbackRef.current;

    // setupAudio: Request access to the user's microphone and call setupStream with the audio stream.
    const setupAudio = async () => {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
          });
          setupStream(stream);
        } catch (err) {
          console.error(err);
        }
      }
    };

    // setupStream: Initialize MediaRecorder, collect audio data into chunks, and process into an audio blob when recording stops.
    const setupStream = (stream) => {
      recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/mp3; codecs=opus' });
        setAudioBlob(blob);
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;
      };
      canRecord = true;
    };

    // toggleMic: Start or stop audio recording based on recorder's state and update mic button appearance.
    const toggleMic = () => {
      if (!canRecord) return;
      if (recorder.state === 'inactive') {
        recorder.start();
        micButton.classList.add('is-recording');
      } else {
        recorder.stop();
        micButton.classList.remove('is-recording');
      }
    };

    micButton.addEventListener('click', toggleMic);
    setupAudio();

    return () => {
      micButton.removeEventListener('click', toggleMic);
    };
  }, [audioBlob]);

  const handleTestQuery = async () => {
    const randomIndex = Math.floor(Math.random() * 17); 
    const audioModule = await import(`./assets/${randomIndex}.mp3`);
    const response = await fetch(audioModule.default);
    const blob = await response.blob();
    setAudioBlob(blob);
    const audioURL = window.URL.createObjectURL(blob);
    playbackRef.current.src = audioURL;

  };

  // handleButtonClick: Send the audio blob to the backend for processing and navigate to the results page.
  const handleButtonClick = async () => {
    setIsClicked(true);
    setSearchText('Searching ...');
    const formData = new FormData();
    formData.append('audioFile', audioBlob, 'recording.mp3');

    try {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/upload`,
        {
          method: 'POST',
          body: formData,
          mode: 'cors',
        }
      );

      const jsonData = await response.json();
      setTrackInfo(jsonData);
      navigate('/results', { state: { trackInfo: jsonData.tracks } });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <main>
      <h1>Sing, Hum, or Play to find your song</h1>
      <p>
        Click the mic and hum a clear tune of one of the songs in the Astra DB
        song collection, or click random hum.
      </p>
      <button className="mic-toggle" ref={micButtonRef}>
        <span className="material-icons">mic</span>
      </button>
      <div className="controls-container">
      <button className="random-hum"
      onClick={handleTestQuery}> Random hum</button>
        <audio className="playback" controls ref={playbackRef}></audio>
        <button
          className={`search-button ${isClicked ? 'clicked' : ''}`}
          onClick={handleButtonClick}
        >
          {searchText}
        </button>
        
      </div>
    </main>
  );
}

export default Home;
