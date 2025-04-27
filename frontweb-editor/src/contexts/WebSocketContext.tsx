import { createContext, useContext, useEffect, useState } from 'react';
import useWebSocket, { ReadyState, SendMessage  } from 'react-use-websocket';
import { useEditor } from './AppContext';

interface IWebSocketContext {
    sendMessage: SendMessage;
    lastChatMessage: any;
    onlineUsers: any[];
    messageHistory: any[];
    readyState: ReadyState;
  }

const WebSocketContext = createContext<IWebSocketContext | null>(null);

import { ReactNode } from 'react';

export const WebSocketProvider = ({ children }: { children: ReactNode }) => {
  const { editor } = useEditor(); 
  const [userId] = useState(() => sessionStorage.getItem('user_id'));
  const [userEmail] = useState(() => sessionStorage.getItem('user_email'));

  const [lastChatMessage, setLastChatMessage] = useState(null);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(
    userId && userEmail 
      ? `ws://localhost:8000/api/socket/ws/${userId}/${userEmail}`
      : null,
    {
      onOpen: () => console.log('WebSocket conectado'),
      onError: (event) => console.error('Error en WebSocket:', event),
      shouldReconnect: () => true,
      reconnectAttempts: 10,
      reconnectInterval: 3000,
    }
  );
  type IncomingMessage = {
    type: 'users' | 'message' | 'history' | 'editor-update';
    data: any;
  };

  useEffect(() => {
    console.log(lastMessage)
    if (lastMessage !== null) {
      try {
        const data : IncomingMessage = JSON.parse(lastMessage.data);
        console.log("Mensaje recibido:", data);

        if (data.type === 'users') {
          setOnlineUsers(data.data); // 👈 usuarios conectados
        } 
        else if (data.type === 'message') {
          setLastChatMessage(data.data); // 👈 último mensaje
        }
        else if (data.type === 'history') {
          setMessageHistory(data.data); // 👈 historial de mensajes
        }
        else if (data.type === 'editor-update') {
          handleEditorUpdate(data.data);  // <<< nueva función que debes crear
        }

      } catch (error) {
        console.error('Error al parsear mensaje:', error);
      }
    }
  }, [lastMessage]);

  const handleEditorUpdate = (update: any) => {
    if (!editor) return;
  
    if (update.action === 'add') {
      console.log('Recibiendo nuevo componente para añadir:', update.component);
      editor.addComponents(update.component);
    }
  
    // Puedes después manejar más acciones: delete, update, move, etc.
  };

  return (
    <WebSocketContext.Provider value={{ 
      sendMessage, 
      lastChatMessage, 
      onlineUsers, 
      messageHistory, 
      readyState 
    }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => {
  return useContext(WebSocketContext);
};
