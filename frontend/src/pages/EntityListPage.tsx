import { Container, Title } from '@mantine/core';
import { useParams } from 'react-router-dom';
import { CategoryView } from '../components/content/CategoryView';
import type { EntityType } from '../components/content/CategoryView';
import { listLocations } from '../api/locations';
import { listRaces } from '../api/races';
import { listCharacters } from '../api/characters';
import { listEvents } from '../api/events';

const CONFIG: Record<EntityType, { label: string; fetch: (pid: number) => Promise<any[]> }> = {
  location: { label: 'Locations', fetch: listLocations },
  race: { label: 'Races', fetch: listRaces },
  character: { label: 'Characters', fetch: listCharacters },
  event: { label: 'Events', fetch: listEvents },
};

export function EntityListPage() {
  const { projectId, entityType } = useParams<{ projectId: string; entityType: string }>();
  const pid = parseInt(projectId ?? '0', 10);
  const type = entityType as EntityType;
  const config = CONFIG[type];

  if (!config) return <Container><Title order={2}>Unknown entity type</Title></Container>;

  return (
    <Container size="lg" py="xl">
      <CategoryView
        projectId={pid}
        entityType={type}
        label={config.label}
        fetchEntities={config.fetch}
      />
    </Container>
  );
}
