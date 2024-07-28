import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import leftArrow from './images/left-arrow.svg';

function Results() {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate('/');
  };

  const location = useLocation();
  const { trackInfo } = location.state || { trackInfo: null };

  if (!trackInfo) {
    return <div>No track info available</div>;
  }

  return (
    <div className="track-info">
      <button className="back-button" onClick={handleBackClick}>
        ⬅
      </button>
      <img src={trackInfo.album_image} alt="Album" />
      <h3>{`${trackInfo.track} - ${trackInfo.artist}`}</h3>
      <h4>{trackInfo.album}</h4>
      <audio controls src={trackInfo.track_url} />
    </div>
  );
}

export default Results;
