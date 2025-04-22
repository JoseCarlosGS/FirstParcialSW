import axios from 'axios';

const API_URL = 'http://localhost:8000/auth'

export const login = async (email: string, password: string) => {
    try {
        const response = await axios.post(`${API_URL}/login`, { email, password });
        localStorage.setItem('token', response.data.access_token)
        return response.data; // Token or user data  
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
};

export const register = async (email: string, password: string) => {
    try {
        const response = await axios.post(`${API_URL}/register`, { email, password });
        return response.data; // Confirmation or user data
    } catch (error) {
        console.error('Register error:', error);
        throw error;
    }
};

export const logout = () => {
    // Clear local storage or cookies
    localStorage.removeItem('token');
};

export const getCurrentUser = () => {
    const token = localStorage.getItem('token');
    if (!token) return null;

    // Decode token or fetch user data
    return token;
};

export const getHeaders = () => {
    const token = localStorage.getItem('token'); // Obtiene el token del almacenamiento local
  
    // Define los encabezados base
    const headers = {
      'Content-Type': 'application/json', // Indica que se envía/recibe JSON
    };
  
    // Si hay un token, añádelo al encabezado "Authorization"
    if (token) {
      return {
        ...headers,
        Authorization: `Bearer ${token}`, // Añade el token en el formato Bearer
      };
    }
  
    // Si no hay token, devuelve solo los encabezados base
    return headers;
  };