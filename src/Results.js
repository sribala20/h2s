import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import leftArrow from './images/left-arrow.svg';

function Results() {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate('/');
  };

  const location = useLocation();
  const { trackInfo } = location.state || { trackInfo: [] };

  if (!trackInfo || trackInfo.length === 0) {
    return <div>No track info available</div>;
  }

  return (
    <div>
      <div className="track-info">
        <button className="back-button" onClick={handleBackClick}>
          ⬅
        </button>
        <img src={trackInfo[0].album_image} alt="Album" />
        <h3>{`${trackInfo[0].track} - ${trackInfo[0].artist}`}</h3>
        <h4>{trackInfo[0].album}</h4>
        <audio controls src={trackInfo[0].track_url} />
      </div>
      <div className="songs-header">Other Matches :</div>
      <div className="songs-gallery">
        {trackInfo.slice(1, 5).map((track, index) => (
          <div key={index} className="song-bubble">
            <p>
              {track.track} - {track.artist}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;
