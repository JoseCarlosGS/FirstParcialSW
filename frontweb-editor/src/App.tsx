import React from 'react';
import Router from './Router.tsx'
import { AppProvider} from './contexts/AppContext.tsx';

const App: React.FC = () => {
  return (
    <div className="App">
      <AppProvider>
        <Router />
      </AppProvider>
    </div>
  );
};

export default App;
