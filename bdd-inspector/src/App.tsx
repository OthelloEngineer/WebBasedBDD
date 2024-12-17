import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FileInspector from './component/FileInspector';
import DependencyManager from './component/DependencyManager';
import './App.css';
function App() {
  return (
    <Router>
      <div className="App">
<header className="App-header">
  <h1 style={
    {
      color: 'white',
    }
  }>BDD inspector for End Users</h1>
  <nav>
    <ul className="nav-list">
      <li><Link to="/">Home</Link></li>
      <li><Link to="/file-inspector">BDD History</Link></li>
      <li><Link to="/dependency-manager">Dependency Manager</Link></li>
    </ul>
  </nav>
</header>

        
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/file-inspector" element={<FileInspector />} />
            <Route path="/dependency-manager" element={<DependencyManager />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home() {
  return <div>
    <h2>Welcome to an AI-driven analytics website for your Behaviour Driven Development Cobot Scenarious </h2>
    <img src="https://rbtx.com/_next/image?url=https%3A%2F%2Fa.storyblok.com%2Ff%2F298593%2F2b9a1e9875%2Fcobot_family_e-series_ur20.png&w=3840&q=75"
    alt="AI-driven analytics" />
     </div>;
}

export default App;
