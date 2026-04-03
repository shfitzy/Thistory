import { useEffect, useState } from 'react';
import { Container, Loader, Title } from '@mantine/core';
import { useNavigate, useParams } from 'react-router-dom';
import { EntityForm } from '../components/content/EntityForm';
import type { EntityType } from '../components/content/CategoryView';
import { getLocation, updateLocation } from '../api/locations';
import { getRace, updateRace } from '../api/races';
import { getCharacter, updateCharacter } from '../api/characters';
import { getEvent, updateEvent } from '../api/events';

const fetchers: Record<EntityType, (pid: number, id: number) => Promise<any>> = {
  location: getLocation,
  race: getRace,
  character: getCharacter,
  event: getEvent,
};

const updaters: Record<EntityType, (pid: number, id: number, data: any) => Promise<any>> = {
  location: updateLocation,
  race: updateRace,
  character: updateCharacter,
  event: updateEvent,
};

const LABELS: Record<EntityType, string> = {
  location: 'Location',
  race: 'Race',
  character: 'Character',
  event: 'Event',
};

export function EditEntityPage() {
  const { projectId, entityType, entityId } = useParams<{ projectId: string; entityType: string; entityId: string }>();
  const navigate = useNavigate();
  const pid = parseInt(projectId ?? '0', 10);
  const eid = parseInt(entityId ?? '0', 10);
  const type = entityType as EntityType;

  const [entity, setEntity] = useState<Record<string, any> | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchers[type]?.(pid, eid).then(setEntity).catch(() => {});
  }, [pid, type, eid]);

  if (!entity) return <Container py="xl"><Loader /></Container>;

  const handleSubmit = async (values: Record<string, any>) => {
    setLoading(true);
    try {
      await updaters[type](pid, eid, values);
      navigate(`/projects/${pid}/${type}s/${eid}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="sm" py="xl">
      <Title order={2} mb="lg">Edit {LABELS[type]}</Title>
      <EntityForm
        projectId={pid}
        entityType={type}
        initialValues={entity}
        onSubmit={handleSubmit}
        onCancel={() => navigate(`/projects/${pid}/${type}s/${eid}`)}
        loading={loading}
      />
    </Container>
  );
}
