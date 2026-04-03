import { useState } from 'react';
import { Container, Title } from '@mantine/core';
import { useNavigate, useParams } from 'react-router-dom';
import { EntityForm } from '../components/content/EntityForm';
import type { EntityType } from '../components/content/CategoryView';
import { createLocation } from '../api/locations';
import { createRace } from '../api/races';
import { createCharacter } from '../api/characters';
import { createEvent } from '../api/events';

const creators: Record<EntityType, (pid: number, data: any) => Promise<any>> = {
  location: createLocation,
  race: createRace,
  character: createCharacter,
  event: createEvent,
};

const LABELS: Record<EntityType, string> = {
  location: 'Location',
  race: 'Race',
  character: 'Character',
  event: 'Event',
};

export function CreateEntityPage() {
  const { projectId, entityType } = useParams<{ projectId: string; entityType: string }>();
  const navigate = useNavigate();
  const pid = parseInt(projectId ?? '0', 10);
  const type = entityType as EntityType;
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: Record<string, any>) => {
    setLoading(true);
    try {
      const entity = await creators[type](pid, values);
      navigate(`/projects/${pid}/${type}s/${entity.id}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="sm" py="xl">
      <Title order={2} mb="lg">New {LABELS[type]}</Title>
      <EntityForm
        projectId={pid}
        entityType={type}
        onSubmit={handleSubmit}
        onCancel={() => navigate(`/projects/${pid}/${type}s`)}
        loading={loading}
      />
    </Container>
  );
}
