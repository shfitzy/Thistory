import { apiClient as client } from './client';

export interface Project {
  id: number;
  user_id: number;
  title: string;
  short_description: string;
  long_description: string;
  visibility: 'private' | 'public';
  created_at: string;
  updated_at?: string;
}

export interface ProjectCreate {
  title: string;
  short_description: string;
  long_description: string;
  visibility?: 'private' | 'public';
}

export interface ProjectUpdate {
  title?: string;
  short_description?: string;
  long_description?: string;
  visibility?: 'private' | 'public';
}

export const createProject = async (data: ProjectCreate): Promise<Project> => {
  const response = await client.post('/api/v1/projects', data);
  return response.data;
};

export const getProjects = async (): Promise<Project[]> => {
  const response = await client.get('/api/v1/projects');
  return response.data;
};

export const getProject = async (id: number): Promise<Project> => {
  const response = await client.get(`/api/v1/projects/${id}`);
  return response.data;
};

export const updateProject = async (id: number, data: ProjectUpdate): Promise<Project> => {
  const response = await client.put(`/api/v1/projects/${id}`, data);
  return response.data;
};

export const deleteProject = async (id: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${id}`);
};

export const updateProjectVisibility = async (
  id: number,
  visibility: 'private' | 'public'
): Promise<Project> => {
  const response = await client.patch(`/api/v1/projects/${id}/visibility`, { visibility });
  return response.data;
};

export const getAllProjects = async (): Promise<Project[]> => {
  const response = await client.get('/api/v1/admin/projects');
  return response.data;
};
