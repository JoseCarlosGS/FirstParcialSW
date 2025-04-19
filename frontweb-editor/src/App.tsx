import React from 'react';
import Editor from './views/editor/components/Editor';

const App: React.FC = () => {
  return (
    <div className="App">
      <h2 style={{ textAlign: 'center' }}>Editor Web con GrapesJS</h2>
      <Editor />
    </div>
  );
};

export default App;
