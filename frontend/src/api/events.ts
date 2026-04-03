import { apiClient as client } from './client';

export interface Event {
  id: number;
  project_id: number;
  name: string;
  event_date?: string;
  event_date_end?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface EventCreate {
  name: string;
  event_date: string;
  event_date_end?: string;
  description?: string;
}

export interface EventUpdate {
  name?: string;
  event_date?: string;
  event_date_end?: string;
  description?: string;
}

export const listEvents = async (projectId: number, skip = 0, limit = 50): Promise<Event[]> => {
  const response = await client.get(`/api/v1/projects/${projectId}/events`, { params: { skip, limit } });
  return response.data;
};

export const getEvent = async (projectId: number, eventId: number): Promise<Event> => {
  const response = await client.get(`/api/v1/projects/${projectId}/events/${eventId}`);
  return response.data;
};

export const createEvent = async (projectId: number, data: EventCreate): Promise<Event> => {
  const response = await client.post(`/api/v1/projects/${projectId}/events`, data);
  return response.data;
};

export const updateEvent = async (projectId: number, eventId: number, data: EventUpdate): Promise<Event> => {
  const response = await client.put(`/api/v1/projects/${projectId}/events/${eventId}`, data);
  return response.data;
};

export const deleteEvent = async (projectId: number, eventId: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${projectId}/events/${eventId}`);
};
