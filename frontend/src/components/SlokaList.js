// SlokaList.js
import React, { useState } from 'react';

function SlokaList() {
  const [slokas, setSlokas] = useState([]);

  const fetchSlokas = (chapterId) => {
    fetch(`http://localhost:8000/slokas/${chapterId}`)
      .then(response => response.json())
      .then(data => setSlokas(data));
  };

  return (
    <div>
      <button onClick={() => fetchSlokas(1)}>Get Slokas for Chapter 1</button>
      <ul className="sloka-list">
        {slokas.map(sloka => (
          <li key={sloka.id} className="sloka-item">
            {sloka.sloka_text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SlokaList;
