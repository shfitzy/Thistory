import { apiClient as client } from './client';

export interface Relationship {
  id: number;
  project_id: number;
  from_entity_type: string;
  from_entity_id: number;
  to_entity_type: string;
  to_entity_id: number;
  relationship_type?: string;
  description?: string;
  created_at: string;
}

export interface RelationshipCreate {
  from_entity_type: string;
  from_entity_id: number;
  to_entity_type: string;
  to_entity_id: number;
  relationship_type?: string;
  description?: string;
}

export const listRelationships = async (
  projectId: number,
  entityType: string,
  entityId: number
): Promise<Relationship[]> => {
  const response = await client.get(`/api/v1/projects/${projectId}/relationships`, {
    params: { entity_type: entityType, entity_id: entityId },
  });
  return response.data;
};

export const createRelationship = async (
  projectId: number,
  data: RelationshipCreate
): Promise<Relationship> => {
  const response = await client.post(`/api/v1/projects/${projectId}/relationships`, data);
  return response.data;
};

export const deleteRelationship = async (projectId: number, relationshipId: number): Promise<void> => {
  await client.delete(`/api/v1/projects/${projectId}/relationships/${relationshipId}`);
};
