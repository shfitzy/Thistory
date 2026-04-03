import { apiClient as client } from './client';

export interface Race {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface RaceCreate {
  name: string;
  description?: string;
}

export interface RaceUpdate {
  name?: string;
  description?: string;
}

export const listRaces = async (projectId: number, skip = 0, limit = 50): Promise<Race[]> => {
  const response = await client.get(`/api/v1/projects/${projectId}/races`, { params: { skip, limit } });
  return response.data;
};

export const getRace = async (projectId: number, raceId: number): Promise<Race> => {
  const response = await client.get(`/api/v1/projects/${projectId}/races/${raceId}`);
  return response.data;
};

export const createRace = async (projectId: number, data: RaceCreate): Promise<Race> => {
  const response = await client.post(`/api/v1/projects/${projectId}/races`, data);
  return response.data;
};

export const updateRace = async (projectId: number, raceId: number, data: RaceUpdate): Promise<Race> => {
  const response = await client.put(`/api/v1/projects/${projectId}/races/${raceId}`, data);
  return response.data;
};

export const deleteRace = async (projectId: number, raceId: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${projectId}/races/${raceId}`);
};
