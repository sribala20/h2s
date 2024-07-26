// Search.js
import React, { useState } from 'react';
import axios from 'axios';
// import Recorder from './Recorder';

const Search = () => {
  const [result, setResult] = useState(null);

  const handleStop = async (blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'recording.mp3');

    try {
      const response = await axios.post('/api/search', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error performing search', error);
    }
  };

  return (
    <div>
      {/* <Recorder onStop={handleStop} /> */}
      {result && <div>Search Result: {result}</div>}
    </div>
  );
};

export default Search;
