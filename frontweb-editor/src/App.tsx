import React from 'react';
import Router from './Router.tsx'
import { AppProvider} from './contexts/AppContext.tsx';
import { WebSocketProvider } from './contexts/WebSocketContext.tsx';

const App: React.FC = () => {
  return (
    <div className="App">
      <AppProvider>
        <WebSocketProvider>
          <Router />
        </WebSocketProvider>
      </AppProvider>
    </div>
  );
};

export default App;
