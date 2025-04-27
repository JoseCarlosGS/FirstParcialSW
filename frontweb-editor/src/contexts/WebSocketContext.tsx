import { createContext, useContext, useEffect, useState } from 'react';
import useWebSocket, { ReadyState, SendMessage  } from 'react-use-websocket';

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

  useEffect(() => {
    console.log(lastMessage)
    if (lastMessage !== null) {
      try {
        const data = JSON.parse(lastMessage.data);
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

      } catch (error) {
        console.error('Error al parsear mensaje:', error);
      }
    }
  }, [lastMessage]);

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
