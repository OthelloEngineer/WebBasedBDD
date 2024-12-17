import React, { useState, useEffect } from 'react';

export interface FileChange {
  file_name: string;
  commit_sha: string;
  before: string;
  after: string;
  user: string;
  timestamp: string;
  dependencies?: number[]; 
}

export default function FileInspector() {
  const [changes, setChanges] = useState<FileChange[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<string>('');
  const [currentFileInput, setCurrentFileInput] = useState<string>('');
  const [currentUserInput, setCurrentUserInput] = useState<string>('');
  const [currentUser, setCurrentUser] = useState<string>("general");
  useEffect(() => {
    getChanges();
  }, [currentFile]);

  function getChanges() {
    fetch('http://localhost:8000/get_changes/' + currentFile)
      .then(response => {
        console.log("specfici file req:", currentFile)
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json() as Promise<FileChange[]>;
      })
      .then(data => {
        console.log('Changes:', data);
        setChanges(data);
      })
      .catch(err => {
        setError(err.message);
        setChanges([]);
        console.error('Error fetching changes:', err);
      });
  }

    useEffect(() => {
    fetch('http://localhost:8000/get_actor')
        .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
        })
        .then(data => {
        console.log('Current user:', data.actor_name);
        setCurrentUser(data.actor_name);
        getChanges();
        })
        .catch(error => {
        console.error('Error fetching current user:', error);
        });
    }, []);

    function setNewUser(actorName: string) {
    const actorEmail = 'random@example.com';

    const url = `http://localhost:8000/set_actor?actor_name=${encodeURIComponent(actorName)}&actor_email=${encodeURIComponent(actorEmail)}`;

    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
    })
        .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
        })
        .then(data => {
        console.log('User set successfully:', data);
        setCurrentUser(actorName);
        return data.actor_name;
        })
        .catch(error => {
        console.error('Error setting current user:', error);
        return 'General';
        });
    }

  return (
<div style={styles.changeContainer}>
  <h1>BDD revision service</h1>
  
  <div style={{ marginBottom: '10px' }}>
    <input 
      type="text" 
      placeholder={currentFileInput} 
      onChange={(e) => setCurrentFileInput(e.target.value)} 
      style={{ marginRight: '10px', padding: '6px', borderRadius: '4px', border: '1px solid #ccc',
                        boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.35)', // Add a subtle drop shadow
       }}
      
    />
    <button
      style={styles.button}
      onClick={() => {
        setCurrentFile(currentFileInput);
        console.log("currentFileInput:", currentFileInput);
      }}
    >
      Inspect
    </button>
  </div>
  
  <div style={{ marginBottom: '10px' }}>
    <input 
      type="text" 
      placeholder={currentUserInput} 
      onChange={(e) => setCurrentUserInput(e.target.value)} 
      style={{ marginRight: '10px', padding: '6px', borderRadius: '4px', border: '1px solid #ccc',
            boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.3)', // Add a subtle drop shadow
       }}
    />
    <button
      style={styles.button}
      onClick={() => {
        setNewUser(currentUserInput);
        console.log("currentUserInput:", currentUserInput);
      }}
    >
      Change User
    </button>
  </div>

  <p>
    {currentFile === '' 
      ? `inspected changes in BDDs in the last 10 days made by user: ${currentUser}` 
      : `inspecting BDD: ${currentFile}`}
  </p>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {!error && changes.length === 0 && <p>No changes or Loading revision history...</p>}

      {!error && changes.length > 0 && (
        <div>
          {changes.map((change: FileChange, index: number) => (
            <div key={index} style={styles.changeContainer}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}> 
                <div 
                  style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <p>
                    <strong>User:</strong> {change.user} -  <strong>Time: </strong> {change.timestamp}  - <strong> Dependencies:</strong> {change.dependencies?.join(", ") || "None"}
                  </p>
                  <p>
                    <strong>File Name:</strong> {change.file_name}
                  </p>
                  <p>
                  <strong> Change ID:</strong> {change.commit_sha} 
                  </p>
                </div>
                <div>
                  <button style={styles.button} >
                    Revert this change
                  </button>
                </div>
              </div>
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
    border: '1px solid #2D174C55',
    padding: '15px',
    marginBottom: '20px',
    borderRadius: '5px',
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.3)', // Add a subtle drop shadow
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
    background: 'linear-gradient(to bottom, #ffffff 0%, #c0c0c0 100%)',
    padding: '10px',
    borderRadius: '4px',
    border: '2px solid #3c0857',
    overflowX: 'auto',
    textAlign: 'left',
    alignItems: 'left',
    justifyContent: 'left',
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.3)', // Add a subtle drop shadow

  },
  button: {
    backgroundColor: '#32405C',
    border: 'none',
    color: '#fff',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'background-color 0.3s ease, transform 0.3s ease',
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.3)', // Add a subtle drop shadow
  },
};
