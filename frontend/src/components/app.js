// App.js
import React, { useState, useEffect } from 'react';
import SlokaList from './components/SlokaList';

function App() {
  const [chapters, setChapters] = useState([]);

  useEffect(() => {
    fetch("/api/chapters")
      .then(response => response.json())
      .then(data => setChapters(data));
  }, []);

  return (
    <div className="App">
      <h1>Bhagavad Gita Explorer</h1>
      <ul>
        {chapters.map(chapter => (
          <li key={chapter.id}>{chapter.name}</li>
        ))}
      </ul>
      <SlokaList />
    </div>
  );
}

export default App;
