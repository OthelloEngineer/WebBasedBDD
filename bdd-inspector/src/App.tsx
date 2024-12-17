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
  }>My Application</h1>
  <nav>
    <ul className="nav-list">
      <li><Link to="/">Home</Link></li>
      <li><Link to="/file-inspector">File Inspector</Link></li>
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
  return <h2>Welcome to My Application</h2>;
}

export default App;
