import axios, { AxiosResponse } from 'axios';
import { Project } from "../interfaces/Project";
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

}