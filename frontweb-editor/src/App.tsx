import React from 'react';
import Router from './Router.tsx'

const App: React.FC = () => {
  return (
    <div className="App">
      <h2 style={{ textAlign: 'center' }}>Editor Web con GrapesJS</h2>
      <Router />
    </div>
  );
};

export default App;
