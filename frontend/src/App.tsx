import React from 'react';
import Dashboard from "./Dashboard";
import Header from './Header';

const App: React.FC = () => {
  return (
    <div>
      <Header />
      <Dashboard />
      <footer>
        <p>&copy; 2025 Home Agent</p>
      </footer>
    </div>
  );
};

export default App;
