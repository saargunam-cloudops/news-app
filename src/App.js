// Edit <code>src/App.js</code> and save to reload.
// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p> 
//           Happy coding !
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React 2024!!
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


import React, { useState, useEffect } from 'react';

const App = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    // Fetch articles from the backend API
    fetch('/api/articles')
      .then(response => response.json())
      .then(data => setArticles(data.articles))
      .catch(error => console.error('Error fetching articles:', error));
  }, []);

  return (
    <div>
      <h1>DevOps News Aggregator</h1>
      <ul>
        {articles.map(article => (
          <li key={article.id}>{article.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;