import React, { useEffect, useRef, useState } from 'react';
import { useEditor } from '../../contexts/AppContext';
import { User } from 'lucide-react';
import { Settings } from 'lucide-react';
import { LogOut } from 'lucide-react';
import { logout } from '../../services/LoginServices';
import { useNavigate } from 'react-router-dom';


const Navbar: React.FC = () => {
  const { editor } = useEditor();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const closeMenu = () => setMenuOpen(false);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      closeMenu();
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleExport = async () => {
    if (!editor) return;
    
    try {
      // Intenta obtener los datos del proyecto usando el método correcto
      // GrapesJS Studio parece usar un método diferente para obtener los datos del proyecto
      const data = await editor.Projects?.getCurrent()?.getData();
      
      // Si no existe, intenta con otras alternativas comunes en GrapesJS
      const projectData = data || editor.getProjectData?.() || editor.Projects?.getProjectData?.();
      
      if (!projectData) {
        console.error('No se pudieron obtener los datos del proyecto');
        return;
      }
      
      // Crear un archivo para descargar
      const blob = new Blob([JSON.stringify(projectData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
  
      // Descargar el archivo
      const a = document.createElement('a');
      a.href = url;
      a.download = 'proyecto.json';
      a.click();
      URL.revokeObjectURL(url);
      
      console.log('Proyecto exportado con éxito');
    } catch (error) {
      console.error('Error al exportar el proyecto:', error);
    }
  };

  const handleImportClick = () => {
    console.log('Clic en Importar');
    fileInputRef.current?.click();
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log('onChange');
  
    const file = event.target.files?.[0];
    console.log('Archivo cargado:', file);
    if (!file || !editor) return;
  
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const result = e.target?.result;
        if (typeof result !== 'string') {
          console.error('Resultado de lectura no válido');
          return;
        }
        
        const json = JSON.parse(result);
        
        // Intenta diferentes métodos para cargar los datos del proyecto
        if (editor.Projects?.getCurrent()?.setData) {
          await editor.Projects.getCurrent().setData(json);
        } else if (editor.loadProjectData) {
          await editor.loadProjectData(json);
        } else if (editor.Projects?.loadProjectData) {
          await editor.Projects.loadProjectData(json);
        } else {
          console.error('No se encontró un método válido para cargar los datos del proyecto');
          return;
        }
        
        console.log('Proyecto importado con éxito');
      } catch (error) {
        console.error('Error al procesar el archivo:', error);
      }
    };
    
    reader.readAsText(file);
    event.target.value = '';
  };

  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  const handleLogout = async () =>{
    await logout()
    navigate('/')
  }

  return (
    <nav className="bg-gray-900 text-white px-4 py-1.5 relative z-50 border-b border-gray-800 border-radius-2">
    <div className="flex items-center justify-between h-12">
      {/* Izquierda: Logo y menú Proyecto */}
      <div className="flex items-center space-x-3">
        <div className="text-lg font-semibold text-white">MiDashboard</div>
        <div className="inline-block relative">
          <button
            onClick={toggleMenu}
            className="appearance-none text-white text-sm font-medium focus:outline-none bg-transparent"
          >
            Proyecto ▼
          </button>

          {menuOpen && (
            <div className="absolute bg-gray-800 text-sm text-white mt-1.5 py-1 rounded shadow-lg z-50 w-36">
              <div
                onClick={() => {
                  handleImportClick();
                  closeMenu();
                }}
                className="px-3 py-1 hover:bg-gray-700 cursor-pointer"
              >
                Importar
              </div>
              <div
                onClick={() => {
                  handleExport();
                  closeMenu();
                }}
                className="px-3 py-1 hover:bg-gray-700 cursor-pointer"
              >
                Exportar
              </div>
            </div>
          )}
          <input
            type="file"
            accept=".json"
            ref={fileInputRef}
            className="hidden"
            onChange={handleImport}
          />
        </div>
      </div>

      {/* Derecha: Avatar de usuario */}
      <div className="relative">
        <button 
          onClick={toggleUserMenu}
          className="flex items-center space-x-2 bg-transparent hover:bg-transparent appearance-none"
        >
          <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-sm font-bold">
            JD
          </div>
        </button>
        
        {showUserMenu && (
          <div className="absolute right-0 mt-1 w-44 bg-gray-800 rounded-md shadow-lg py-1 z-10 text-sm text-white">
            <a href="#" className="flex items-center px-3 py-1 hover:bg-gray-700 text-white">
              <User size={14} className="mr-2" />
              Perfil
            </a>
            <a href="#" className="flex items-center px-3 py-1 hover:bg-gray-700 text-white">
              <Settings size={14} className="mr-2" />
              Ajustes
            </a>
            <a href="#" onClick={handleLogout} className="flex items-center px-3 py-1 hover:bg-gray-700 text-white">
              <LogOut size={14} className="mr-2" />
              Cerrar Sesión
            </a>
          </div>
        )}
      </div>
    </div>
  </nav>

  );
};

export default Navbar;
