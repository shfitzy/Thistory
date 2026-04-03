import { apiClient } from './client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
  updated_at: string;
}

export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const response = await apiClient.post<User>('/api/v1/auth/register', data);
    return response.data;
  },
};

export type { User };