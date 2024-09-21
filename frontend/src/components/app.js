// App.js
import React, { useState, useEffect } from 'react';
import './styles.css';
import SlokaList from './components/SlokaList';

function App() {
  const [chapters, setChapters] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/chapters/")
      .then(response => response.json())
      .then(data => setChapters(data));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Bhagavad Gita Explorer</h1>
      </header>
      <main>
        <h2>Chapters</h2>
        <ul className="chapter-list">
          {chapters.map(chapter => (
            <li key={chapter.id} className="chapter-item">
              {chapter.name}
            </li>
          ))}
        </ul>
        <SlokaList />
      </main>
    </div>
  );
}

export default App;
