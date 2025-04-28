import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Page {
  get: (property: string) => any;
  getMainComponent: () => any;
  [key: string]: any;
}

interface EditorInstance {
  Pages?: {
    getSelected: () => Page | null;
    getAll: () => Page[];
    add: (pageData: any, options?: any) => Page;
    remove: (page: Page) => void;
    select: (page: Page) => void;
  };
  Storage?: {
    loadProjectData: (data: any) => Promise<any>;
    getProjectData: () => any;
  };
  getWrapper: () => any;
  getComponents: () => any;
  getHtml: () => string;
  getCss: () => string;
  addComponents: (components: any) => any;
  on: (event: string, callback: Function) => void;
  off: (event: string, callback: Function) => void;
  trigger: (event: string, ...args: any[]) => void;
  Commands: {
    add: (name: string, command: any) => void;
    run: (name: string, ...args: any[]) => any;
  };
  [key: string]: any;
  CssComposer?: {
    getAll: () => any[];
    toCSS: (options?: { avoidProtected?: boolean; keepUnusedStyles?: boolean ; rules?: any[]}) => string;
  };
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