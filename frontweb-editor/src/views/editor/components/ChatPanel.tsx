import React, { useState, useRef, useEffect } from 'react';
import { UserCircle, MessageSquare, ChevronLeft, ChevronRight, Send, Plus } from 'lucide-react';
import { ProjectServices } from '../../../services/ProjectServices';
import { User } from '../../../interfaces/User';

// Definición de tipos

interface Message {
  id: string;
  userId: string;
  text: string;
  timestamp: Date;
}

const sampleMessages: Message[] = [
  { id: '1', userId: '1', text: 'Hola a todos, estoy editando la sección de navegación', timestamp: new Date('2025-04-21T11:30:00') },
  { id: '2', userId: '3', text: 'Yo estoy trabajando en el footer', timestamp: new Date('2025-04-21T11:32:00') },
  { id: '3', userId: '2', text: 'Acabo de terminar el diseño del header', timestamp: new Date('2025-04-21T11:35:00') },
];

const ChatPanel: React.FC<any> = (projectId) => {
  // Estados
  const [isOpen, setIsOpen] = useState(true);
  const [users, setUsers] = useState<User[] | undefined>(undefined);
  const [messages, setMessages] = useState<Message[]>(sampleMessages);
  const [newMessage, setNewMessage] = useState('');
  const messageEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (projectId !== null) {
      const fetchUsers = async () => {
        try {
          const data = await ProjectServices.getAllUsersByProjectId(projectId.project);
          setUsers(data);
        } catch (error) {
          console.error('Error al obtener usuarios:', error);
        }
      };

      fetchUsers();
    }
  }, [projectId]);
  
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (newMessage.trim() === '') return;
    
    const message: Message = {
      id: Date.now().toString(),
      userId: '1', // ID del usuario actual (ejemplo)
      text: newMessage,
      timestamp: new Date()
    };
    
    setMessages([...messages, message]);
    setNewMessage('');
  };

  // Formateador de tiempo
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Formatear "visto por última vez"
  const formatLastSeen = (date?: Date) => {
    if (!date) return 'Desconectado';
    
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.round(diffMs / 60000);
    
    if (diffMins < 1) return 'Hace un momento';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    
    return formatTime(date);
  };

    return (
      <div className="h-full relative z-20">
      {/* Botón fijo a la izquierda de la pantalla */}
      {!isOpen && (
        <div className="fixed top-0.9 left-0 transform -translate-y-1/2">
          <button
            onClick={() => setIsOpen(true)}
            className="bg-gray-700 text-white rounded-r-md shadow-md opacity-30 hover:opacity-100 transition-opacity duration-300 w-8 h-10 flex items-center justify-center"
          >
            ☰
          </button>
        </div>
      )}

        {/* Panel principal */}

        <div
          className={`bg-gray-900 border-r border-gray-900 flex flex-col transition-all duration-200 ${
            isOpen ? "w-64" : "w-0 h-0"
          } ${!isOpen ? "overflow-hidden" : ""}`}
          style={{ minWidth: 0 }}
        >
          <div className="flex items-center justify-between border-b border-gray-800">
            <h2 className="font-bold text-white flex items-center m-4">
              Proyecto
            </h2>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-300 hover:text-gray-200"
            >
              {isOpen ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
            </button>
          </div>

          {/* Sección de usuarios */}
          <div className="p-3 border-b border-gray-200">
            <div className="flex items-center justify-between mb-4">
              {/* Título con ícono */}
              <h2 className="font-semibold text-white flex items-center">
                <UserCircle className="mr-2" size={18} />
                Miembros ({users?.filter((u) => u.is_active).length}/{users?.length})
              </h2>

              {/* Botón más pequeño y alineado a la derecha */}
              <button
                type="button"
                className="flex items-center text-xs text-gray-400 hover:text-white hover:bg-gray-700 font-medium rounded-md px-2 py-1 space-x-1 transition-colors"
              >
                <Plus size={14} />
                <span>Añadir</span>
              </button>
            </div>

            <div className="max-h-48 overflow-y-auto">
              {users?.map((user) => (
                <div
                  key={user.id}
                  className="flex items-center py-2 hover:bg-gray-800 rounded-md px-2"
                >
                  <div className="relative mr-2">
                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                      <span className="text-white font-bold text-lg">
                      {user.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span
                      className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${
                        user.is_active ? "bg-green-500" : "bg-gray-400"
                      }`}
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-200 truncate">
                      {user.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {user.is_active
                        ? "En línea"
                        : formatLastSeen(user.last_login ? new Date(user.last_login) : undefined)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Sección de chat */}
          <div className="flex-1 flex flex-col overflow-hidden p-3 bg-gray-900">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-white flex items-center">
                <MessageSquare className="mr-2" size={18} />
                Chat
              </h2>
            </div>

            {/* Mensajes */}
            <div className="flex-1 overflow-y-auto mb-4 pr-2 max-h-74">
              {messages.map((message) => {
                const user = users?.find((u) => u.id.toString() === message.userId);
                const isCurrentUser = message.userId === "1"; // Ejemplo, ajustar a lógica real

                return (
                  <div
                    key={message.id}
                    className={`mb-3 flex ${
                      isCurrentUser ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-xs rounded-lg px-3 py-2 ${
                        isCurrentUser
                          ? "bg-blue-800 text-gray-300 rounded-br-none"
                          : "bg-gray-700 text-gray-300 rounded-bl-none"
                      }`}
                    >
                      {!isCurrentUser && (
                        <p className="text-xs font-bold mb-1 text-white">
                          {user?.name || "Usuario"}
                        </p>
                      )}
                      <p className="text-sm">{message.text}</p>
                      <p
                        className={`text-xs mt-1 ${
                          isCurrentUser ? "text-blue-100" : "text-gray-500"
                        }`}
                      >
                        {formatTime(message.timestamp)}
                      </p>
                    </div>
                  </div>
                );
              })}
              <div ref={messageEndRef} />
            </div>

            {/* Input de mensaje */}
            <div className="flex items-center bg-white rounded-lg border border-gray-300 overflow-hidden">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Escribe un mensaje..."
                className="flex-1 py-2 px-3 focus:outline-none text-sm"
              />
              <button
                onClick={handleSendMessage}
                className="bg-blue-500 hover:bg-blue-600 text-white p-2"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
};

    export default ChatPanel;