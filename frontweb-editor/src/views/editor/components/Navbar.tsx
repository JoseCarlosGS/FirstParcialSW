import React, { useEffect, useRef, useState } from 'react';
import { useEditor } from '../../../contexts/AppContext';

const Navbar: React.FC = () => {
  const editor = useEditor();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [menuOpen, setMenuOpen] = useState(false);

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
    fileInputRef.current?.click();
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !editor) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const json = JSON.parse(e.target?.result as string);
      editor.loadProjectData(json);
    };
    reader.readAsText(file);
  };

  return (
    <nav className="bg-gray-800 text-white px-4 py-3 relative z-50">
        <div className="inline-block relative">
            <button
            onClick={toggleMenu}
            className="text-white text-lg font-medium focus:outline-none"
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
                <input
                type="file"
                accept=".json"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleImport}
                />
            </div>
            )}
        </div>
    </nav>

  );
};

export default Navbar;
