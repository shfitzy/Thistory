import { useEffect, useState } from 'react';
import { Container, Loader, Text } from '@mantine/core';
import { useNavigate, useParams } from 'react-router-dom';
import { EntityDetail } from '../components/content/EntityDetail';
import type { EntityType } from '../components/content/CategoryView';
import { getLocation, deleteLocation } from '../api/locations';
import { getRace, deleteRace } from '../api/races';
import { getCharacter, deleteCharacter } from '../api/characters';
import { getEvent, deleteEvent } from '../api/events';

const fetchers: Record<EntityType, (pid: number, id: number) => Promise<any>> = {
  location: getLocation,
  race: getRace,
  character: getCharacter,
  event: getEvent,
};

const deleters: Record<EntityType, (pid: number, id: number) => Promise<void>> = {
  location: deleteLocation,
  race: deleteRace,
  character: deleteCharacter,
  event: deleteEvent,
};

export function EntityDetailPage() {
  const { projectId, entityType, entityId } = useParams<{ projectId: string; entityType: string; entityId: string }>();
  const navigate = useNavigate();
  const pid = parseInt(projectId ?? '0', 10);
  const eid = parseInt(entityId ?? '0', 10);
  const type = entityType as EntityType;

  const [entity, setEntity] = useState<Record<string, any> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchers[type]?.(pid, eid)
      .then(setEntity)
      .catch(() => setEntity(null))
      .finally(() => setLoading(false));
  }, [pid, type, eid]);

  if (loading) return <Container py="xl"><Loader /></Container>;
  if (!entity) return <Container py="xl"><Text>Not found.</Text></Container>;

  const handleDelete = async () => {
    await deleters[type]?.(pid, eid);
    navigate(`/projects/${pid}/${type}s`);
  };

  return (
    <Container size="lg" py="xl">
      <EntityDetail
        projectId={pid}
        entityType={type}
        entity={entity}
        onEdit={() => navigate(`/projects/${pid}/${type}s/${eid}/edit`)}
        onDelete={handleDelete}
      />
    </Container>
  );
}
