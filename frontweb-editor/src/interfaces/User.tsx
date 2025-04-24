export interface User {
  id: number;
  name: string;
  email: string;
  is_active:boolean;
  created_at:string;
  updated_at:string;
  last_login:string;
  is_superuser:boolean;
}