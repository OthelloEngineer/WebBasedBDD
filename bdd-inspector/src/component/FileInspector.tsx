import React, { useState, useEffect } from 'react';

export interface FileChange {
  file_name: string;
  commit_sha: string;
  before: string;
  after: string;
  user: string;
  timestamp: string;
}

export default function FileInspector() {
  const [changes, setChanges] = useState<FileChange[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<string>('sample.bdd');
  const [currentFileInput, setCurrentFileInput] = useState<string>('sample.bdd');
  useEffect(() => {
    fetch('http://localhost:8000/get_changes/' + currentFile)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json() as Promise<FileChange[]>;
      })
      .then(data => {
        setChanges(data);
      })
      .catch(err => {
        setError(err.message);
        console.error('Error fetching changes:', err);
      });
  }, [currentFile]);



  return (
    <div style={{ padding: '20px' }}>
      <h1>File Inspector</h1>
      <input type="text" placeholder={currentFileInput} onChange={(e) =>  setCurrentFileInput(e.target.value)} />
        <button onClick={() => setCurrentFile(currentFileInput)}>Inspect</button>
      <p>
        Inspecting the file: <strong>sample.bdd</strong>
      </p>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {!error && changes.length === 0 && <p>Loading revision history...</p>}

      {!error && changes.length > 0 && (
        <div>
          {changes.map((change: FileChange, index: number) => (
            <div key={index} style={styles.changeContainer}>
              <h2>Commit: {change.commit_sha}</h2>
              <p>
                <strong>User:</strong> {change.user} -  <strong>Time: </strong> {change.timestamp} 
              </p>
              <p>
                <strong>File Name:</strong> {change.file_name}
              </p>
              <div style={styles.diffContainer}>
                <div style={styles.before}>
                  <h3>Before:</h3>
                  <pre style={styles.codeBlock}>{change.before}</pre>
                </div>
                <div style={styles.after}>
                  <h3>After:</h3>
                  <pre style={styles.codeBlock}>{change.after}</pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  changeContainer: {
    border: '1px solid #ccc',
    padding: '15px',
    marginBottom: '20px',
    borderRadius: '5px',
  },
  diffContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  before: {
    width: '48%',
  },
  after: {
    width: '48%',
  },
  codeBlock: {
    backgroundColor: '#f7f7f7',
    padding: '10px',
    borderRadius: '4px',
    overflowX: 'auto', // Correctly typed
    textAlign: 'left', // Correctly typed
    alignItems: 'left', // Incorrectly typed
    justifyContent: 'left', // Incorrectly typed
  },
};
