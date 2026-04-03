import { apiClient as client } from './client';

export interface Character {
  id: number;
  project_id: number;
  name: string;
  status?: string;
  age?: number;
  race_id?: number;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface CharacterCreate {
  name: string;
  status?: string;
  age?: number;
  race_id?: number;
  description?: string;
}

export interface CharacterUpdate {
  name?: string;
  status?: string;
  age?: number;
  race_id?: number;
  description?: string;
}

export const listCharacters = async (projectId: number, skip = 0, limit = 50): Promise<Character[]> => {
  const response = await client.get(`/api/v1/projects/${projectId}/characters`, { params: { skip, limit } });
  return response.data;
};

export const getCharacter = async (projectId: number, characterId: number): Promise<Character> => {
  const response = await client.get(`/api/v1/projects/${projectId}/characters/${characterId}`);
  return response.data;
};

export const createCharacter = async (projectId: number, data: CharacterCreate): Promise<Character> => {
  const response = await client.post(`/api/v1/projects/${projectId}/characters`, data);
  return response.data;
};

export const updateCharacter = async (projectId: number, characterId: number, data: CharacterUpdate): Promise<Character> => {
  const response = await client.put(`/api/v1/projects/${projectId}/characters/${characterId}`, data);
  return response.data;
};

export const deleteCharacter = async (projectId: number, characterId: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${projectId}/characters/${characterId}`);
};
