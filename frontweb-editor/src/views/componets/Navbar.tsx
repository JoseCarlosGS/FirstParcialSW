import React, { useEffect, useRef, useState } from 'react';
import { useEditor } from '../../contexts/AppContext';
import { User } from 'lucide-react';
import { Settings } from 'lucide-react';
import { LogOut } from 'lucide-react';
import { logout } from '../../services/LoginServices';
import { useNavigate } from 'react-router-dom';


const Navbar: React.FC = () => {
  const editor = useEditor();
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

  const handleExport = () => {
    if (!editor) return;
    const data = editor.getProjectData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'proyecto.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImportClick = () => {
    console.log('Clic en Importar');
    fileInputRef.current?.click();
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log('onChange')

    const file = event.target.files?.[0];
    console.log('Archivo cargado:', event.target.files?.[0]);
    if (!file || !editor) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const json = JSON.parse(e.target?.result as string);
      editor.loadProjectData(json);
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
    <nav className="bg-gray-900 text-white px-4 py-1 relative z-50">
      <div className="flex items-center justify-between">
        {/* Izquierda: Logo y menú Proyecto */}
        <div className="flex items-center space-x-4">
          <div className="text-xl font-bold text-white">MiDashboard</div>
          <div className="inline-block relative">
            <button
              onClick={toggleMenu}
              className="appearance-none text-white text-lg font-medium focus:outline-none bg-transparent"
            >
              Proyecto ▼
            </button>

            {menuOpen && (
              <div className="absolute bg-white text-black mt-2 py-2 rounded shadow-lg z-50 w-40">
                <div
                  onClick={() => {
                    handleImportClick();
                    closeMenu();
                  }}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                >
                  Importar
                </div>
                <div
                  onClick={() => {
                    handleExport();
                    closeMenu();
                  }}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
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
            <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
              JD
            </div>
          </button>
          
          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
              <a href="#" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <User size={16} className="mr-2" />
                Perfil
              </a>
              <a href="#" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <Settings size={16} className="mr-2" />
                Ajustes
              </a>
              <a href="#" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={handleLogout}>
                <LogOut size={16} className="mr-2" />
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
