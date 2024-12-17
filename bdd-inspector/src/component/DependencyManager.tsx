import React, { useState, useEffect } from 'react';

export interface Scenario {
  id: number;
  title: string;
  content: string;
  dependencies: number[];
}

export default function DependencyManager() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [newScenario, setNewScenario] = useState({ title: '', content: '', dependencies: [] });
  const [currentScenarioId, setCurrentScenarioId] = useState<number | null>(null);
  const [dependencyId, setDependencyId] = useState<number | null>(null);
  const [currentUser, setCurrentUser] = useState<string>('general');
  const [currentUserInput, setCurrentUserInput] = useState<string>('');

  useEffect(() => {
    fetchScenarios();
  }, []);

  // Fetch all scenarios from the backend
  function fetchScenarios() {
    fetch('http://localhost:8000/get_all_scenarios')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setScenarios(data);
      })
      .catch(err => {
        setError(err.message);
        setScenarios([]);
        console.error('Error fetching scenarios:', err);
      });
  }

  // Add a new scenario
  function addScenario() {
    fetch('http://localhost:8000/add_scenario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newScenario),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(() => {
        setNewScenario({ title: '', content: '', dependencies: [] });
        fetchScenarios(); // Refresh scenarios
      })
      .catch(err => {
        setError(err.message);
        console.error('Error adding scenario:', err);
      });
  }

  // Add a dependency between scenarios
  function addDependency() {
    if (!currentScenarioId || !dependencyId) {
      alert('Please select both a scenario and a dependency ID.');
      return;
    }

    fetch('http://localhost:8000/set_dependency', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario_id: currentScenarioId,
        dependency_id: dependencyId,
      }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(() => {
        fetchScenarios(); // Refresh scenarios
      })
      .catch(err => {
        setError(err.message);
        console.error('Error adding dependency:', err);
      });
  }

  // Change the current user
  function setNewUser(actorName: string) {
    const actorEmail = 'random@example.com';
    const url = `http://localhost:8000/set_actor?actor_name=${encodeURIComponent(actorName)}&actor_email=${encodeURIComponent(actorEmail)}`;

    fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setCurrentUser(actorName);
      })
      .catch(error => {
        console.error('Error setting current user:', error);
      });
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dependency Manager</h1>

      {/* Add New Scenario Form */}
      <div>
        <h2>Add New Scenario</h2>
        <input
          type="text"
          placeholder="Scenario Title"
          value={newScenario.title}
          onChange={e => setNewScenario({ ...newScenario, title: e.target.value })}
        />
        <textarea
          placeholder="Scenario Content"
          value={newScenario.content}
          onChange={e => setNewScenario({ ...newScenario, content: e.target.value })}
        />
        <button style={styles.button} onClick={addScenario}>Add Scenario</button>
      </div>

      {/* Select Scenario to Add Dependency */}
      <div>
        <h2>Add Dependency</h2>
        <select onChange={e => setCurrentScenarioId(Number(e.target.value))}>
          <option value="">Select Scenario</option>
          {scenarios.map(scenario => (
            <option key={scenario.id} value={scenario.id}>
              {scenario.title} (ID: {scenario.id})
            </option>
          ))}
        </select>
        <input
          type="number"
          placeholder="Dependency ID"
          value={dependencyId || ''}
          onChange={e => setDependencyId(Number(e.target.value))}
        />
        <button style={styles.button} onClick={addDependency}>Add Dependency</button>
      </div>

    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  scenarioContainer: {
    border: '1px solid #ccc',
    padding: '15px',
    marginBottom: '20px',
    borderRadius: '5px',
    gap: '10px',
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
    },
};
