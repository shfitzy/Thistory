import { apiClient as client } from './client';

export interface Location {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface LocationCreate {
  name: string;
  description?: string;
}

export interface LocationUpdate {
  name?: string;
  description?: string;
}

export const listLocations = async (projectId: number, skip = 0, limit = 50): Promise<Location[]> => {
  const response = await client.get(`/api/v1/projects/${projectId}/locations`, { params: { skip, limit } });
  return response.data;
};

export const getLocation = async (projectId: number, locationId: number): Promise<Location> => {
  const response = await client.get(`/api/v1/projects/${projectId}/locations/${locationId}`);
  return response.data;
};

export const createLocation = async (projectId: number, data: LocationCreate): Promise<Location> => {
  const response = await client.post(`/api/v1/projects/${projectId}/locations`, data);
  return response.data;
};

export const updateLocation = async (projectId: number, locationId: number, data: LocationUpdate): Promise<Location> => {
  const response = await client.put(`/api/v1/projects/${projectId}/locations/${locationId}`, data);
  return response.data;
};

export const deleteLocation = async (projectId: number, locationId: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${projectId}/locations/${locationId}`);
};
