import { createContext, useContext } from 'react';
import type { Editor } from 'grapesjs';

export const AppContext = createContext<Editor | null>(null);

export const useEditor = () => useContext(AppContext);