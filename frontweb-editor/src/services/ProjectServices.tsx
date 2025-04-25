import axios, { AxiosResponse } from 'axios';
import { Project, ProjectRequest } from "../interfaces/Project";
import { User } from '../interfaces/User';

const BASE_URL = 'http://localhost:8000/api/project'

export class ProjectServices {

    static async getAllUsersByProjectId(id:number): Promise<User[]> {
        try {
          const response: AxiosResponse<User[]> = await axios.get(`${BASE_URL}/users?project_id=${id}`);
          return response.data;
        } catch (error) {
          console.error('Error fetching users:', error);
          throw error;
        }
    }
    static async getAllProjectsByUserId(id:number): Promise<Project[]> {
        try {
          const response: AxiosResponse<Project[]> = await axios.get(`${BASE_URL}/projects?user_id=${id}`);
          return response.data;
        } catch (error) {
          console.error('Error fetching users:', error);
          throw error;
        }
    }

    static async fetchProjectFile(id: number): Promise<any> {
      const response = await fetch(`${BASE_URL}/load?project_id=${id}`);
      if (!response.ok) {
        throw new Error("No se pudo obtener el archivo desde el backend.");
      }
      return await response.json();
    };

    static async addUserToProject(id:number): Promise<User[]>{
      try{
        const response : AxiosResponse<User[]> = await axios.get(`${BASE_URL}/projects?user_id=${id}`);
        return response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
        throw error;
      }
    } 
    static async createProject(
      userId: number,
      project: ProjectRequest,
      file: File
    ): Promise<any> {
      const formData = new FormData();
      formData.append("file", file);
    
      // Agrega los campos del proyecto al formData
      Object.entries(project).forEach(([key, value]) => {
        formData.append(key, value);
      });
    
      const response = await fetch(`${BASE_URL}/${userId}`, {
        method: "POST",
        body: formData,
      });
    
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error creando el proyecto");
      }
    
      return await response.json();
    }

}