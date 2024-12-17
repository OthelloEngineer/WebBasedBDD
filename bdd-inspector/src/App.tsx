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
      <li>
        
        <Link to="/" style={
          {
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }
        }>Home
        <img src="https://static.thenounproject.com/png/3574480-200.png"
        style={{
          width: '20px',
          height: '20px',
          margin: '0 0 0 10px',
          padding: '5px',
          backgroundColor: 'white',
                        borderRadius: '30%', // Fully rounded corners (circular)
    objectFit: 'cover', // Ensures the image fits within rounded edges
        }}
        ></img>

        </Link>
        
        </li>
      <li><Link to="/file-inspector"
      style={
        {
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center',
        }
      }
      >BDD History

      <img src="https://cdn-icons-png.flaticon.com/512/32/32223.png" style={
        {
          width: '20px',
          height: '20px',
          margin: '0 0 0 10px',
          padding: '5px',
          backgroundColor: 'white',
                        borderRadius: '30%', // Fully rounded corners (circular)
    objectFit: 'cover', // Ensures the image fits within rounded edges
        }
      }></img></Link>
      </li>
      <li><Link to="/dependency-manager"
      style={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
      >Dependency Manager
      
      <img src="https://www.shutterstock.com/image-vector/dependency-icon-thin-linear-style-600nw-2470760659.jpg"
      style={
        {
          width: '20px',
          height: '20px',
          margin: '0 0 0 10px',
          padding: '5px',
          backgroundColor: 'white',
              borderRadius: '30%', // Fully rounded corners (circular)
    objectFit: 'contain', // Ensures the image fits within rounded edges
        }
      }></img>
      
      </Link></li>
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
