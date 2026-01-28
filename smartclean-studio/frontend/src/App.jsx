import React, { useState } from 'react';
import './index.css';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <>
      {!showDashboard ? (
        <LandingPage onStartCleaning={() => setShowDashboard(true)} />
      ) : (
        <Dashboard />
      )}
    </>
  );
}

export default App;
