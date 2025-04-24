import React, { createContext, useContext, useState, ReactNode } from 'react';

// Definimos un tipo para el editor basado en lo que sabemos que necesitaremos
// Se puede expandir según las necesidades específicas
interface EditorInstance {
  // Añade aquí las propiedades y métodos que necesitas usar
  // Por ejemplo:
  Pages?: {
    getSelected: () => any;
  };
  Storage?: {
    loadProjectData: (data: any) => Promise<any>;
    getProjectData: () => any;
  };
  // Añade más propiedades según las necesidades
  [key: string]: any; // Permite acceso a cualquier propiedad desconocida
}

// Definir la interfaz para el valor del contexto
interface AppContextType {
  editor: EditorInstance | null;
  setEditor: (editor: EditorInstance | null) => void;
}

// Crear el contexto con un valor inicial por defecto
const AppContext = createContext<AppContextType | undefined>(undefined);

// Props para el AppProvider
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