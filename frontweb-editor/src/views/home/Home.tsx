import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, PlusCircle, LogOut, User, Settings } from 'lucide-react';
import { Navigate, useNavigate } from 'react-router-dom';

const Home = () => {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const navigate = useNavigate();
  
  // Datos de ejemplo para los proyectos
  const proyectos = [
    { id: 1, nombre: "Proyecto Alpha", descripcion: "Sistema de gestión de inventario", progreso: 75 },
    { id: 2, nombre: "Proyecto Beta", descripcion: "Aplicación de seguimiento de tareas", progreso: 30 },
    { id: 3, nombre: "Proyecto Gamma", descripcion: "Dashboard de analíticas", progreso: 50 },
    { id: 4, nombre: "Proyecto Delta", descripcion: "Sistema de mensajería", progreso: 90 },
    { id: 5, nombre: "Proyecto Epsilon", descripcion: "Plataforma de e-learning", progreso: 15 },
  ];
  
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const nextProject = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % proyectos.length);
  };
  
  const prevProject = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + proyectos.length) % proyectos.length);
  };
  
  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };
  
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-md p-4">
        <div className="flex items-center justify-between">
          <div className="text-xl font-bold text-blue-600">MiDashboard</div>
          <div className="relative">
            <button 
              onClick={toggleUserMenu}
              className="flex items-center space-x-2"
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
                <a href="#" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  <LogOut size={16} className="mr-2" />
                  Cerrar Sesión
                </a>
              </div>
            )}
          </div>
        </div>
      </nav>
      
      {/* Contenido principal */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Mis Proyectos</h1>
            <button 
            className="flex items-center bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
            onClick={() => navigate('/editor')}
            >
            <PlusCircle size={20} className="mr-2" />
            Nuevo Proyecto
            </button>
        </div>
        
        {/* Slider de Proyectos */}
        <div className="bg-white rounded-lg shadow-md p-6 relative">
          <div className="flex items-center">
            <button 
              onClick={prevProject}
              className="absolute left-4 bg-white rounded-full p-2 shadow-md hover:bg-gray-100"
            >
              <ChevronLeft size={24} />
            </button>
            
            <div className="w-full px-12">
              <div className="flex flex-col items-center">
                <h2 className="text-xl font-bold text-gray-800 mb-2">{proyectos[currentIndex].nombre}</h2>
                <p className="text-gray-600 mb-4">{proyectos[currentIndex].descripcion}</p>
                
                <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
                  <div 
                    className="bg-blue-500 h-4 rounded-full"
                    style={{ width: `${proyectos[currentIndex].progreso}%` }}
                  ></div>
                </div>
                
                <div className="text-sm text-gray-600">
                  Progreso: {proyectos[currentIndex].progreso}%
                </div>
                
                <div className="flex space-x-4 mt-6">
                  <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors">
                    Ver Detalles
                  </button>
                  <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md transition-colors">
                    Editar
                  </button>
                </div>
              </div>
            </div>
            
            <button 
              onClick={nextProject}
              className="absolute right-4 bg-white rounded-full p-2 shadow-md hover:bg-gray-100"
            >
              <ChevronRight size={24} />
            </button>
          </div>
          
          {/* Indicadores */}
          <div className="flex justify-center mt-6 space-x-2">
            {proyectos.map((_, index) => (
              <div 
                key={index} 
                className={`h-2 w-2 rounded-full ${currentIndex === index ? 'bg-blue-500' : 'bg-gray-300'}`}
              ></div>
            ))}
          </div>
        </div>
        
        {/* Resumen de Proyectos */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-bold text-lg text-gray-800 mb-2">Proyectos Activos</h3>
            <p className="text-3xl font-bold text-blue-500">{proyectos.length}</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-bold text-lg text-gray-800 mb-2">Completados</h3>
            <p className="text-3xl font-bold text-green-500">2</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="font-bold text-lg text-gray-800 mb-2">Pendientes</h3>
            <p className="text-3xl font-bold text-orange-500">3</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;