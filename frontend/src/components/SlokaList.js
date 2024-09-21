// SlokaList.js
import React, { useState } from 'react';

function SlokaList() {
  const [slokas, setSlokas] = useState([]);

  const fetchSlokas = (chapterId) => {
    fetch(`/api/slokas/${chapterId}`)
      .then(response => response.json())
      .then(data => setSlokas(data));
  };

  return (
    <div>
      <button onClick={() => fetchSlokas(1)}>Get Slokas for Chapter 1</button>
      <ul>
        {slokas.map(sloka => (
          <li key={sloka.id}>{sloka.sloka_text}</li>
        ))}
      </ul>
    </div>
  );
}

export default SlokaList;
