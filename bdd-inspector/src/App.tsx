import React from 'react';
import logo from './logo.svg';
import './App.css';
import FileInspector from './component/FileInspector';
import DependencyManager from './component/DependencyManager';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      </header>
      <h1>File Inspector</h1>
      <FileInspector />
      <div className="flex-container">
        <DependencyManager />
      </div>
    </div>
  );
}

export default App;
