import React, { createContext, useContext, useState, ReactNode } from 'react';

interface EditorInstance {

  Pages?: {
    getSelected: () => any;
  };
  Storage?: {
    loadProjectData: (data: any) => Promise<any>;
    getProjectData: () => any;
  };
  [key: string]: any; 
}

interface AppContextType {
  editor: EditorInstance | null;
  setEditor: (editor: EditorInstance | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

interface AppProviderProps {
  children: ReactNode;
}

// Proveedor del contexto
export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  // Estado para almacenar la instancia del editor
  const [editor, setEditor] = useState<EditorInstance | null>(null);

  // Valores que se proporcionarán a través del contexto
  const contextValue: AppContextType = {
    editor,
    setEditor,
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// Hook personalizado para acceder al contexto
export const useEditor = (): AppContextType => {
  const context = useContext(AppContext);
  
  if (context === undefined) {
    throw new Error('useEditor debe ser usado dentro de un AppProvider');
  }
  
  return context;
};