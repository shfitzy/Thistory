import { useEffect, useState } from 'react';
import { Button, Card, Group, SimpleGrid, Skeleton, Stack, Text, Title } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';

export type EntityType = 'location' | 'race' | 'character' | 'event';

interface CategoryViewProps {
  projectId: number;
  entityType: string;
  label: string;
  fetchEntities: (projectId: number) => Promise<{ id: number; name: string; description?: string }[]>;
}

export function CategoryView({ projectId, entityType, label, fetchEntities }: CategoryViewProps) {
  const navigate = useNavigate();
  const [entities, setEntities] = useState<{ id: number; name: string; description?: string }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEntities(projectId)
      .then(setEntities)
      .finally(() => setLoading(false));
  }, [projectId]);

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={3}>{label}</Title>
        <Button
          leftSection={<IconPlus size={16} />}
          onClick={() => navigate(`/projects/${projectId}/${entityType}/new`)}
        >
          New {label.slice(0, -1)}
        </Button>
      </Group>

      {loading ? (
        <SimpleGrid cols={3}>
          {[1, 2, 3].map(i => <Skeleton key={i} height={80} />)}
        </SimpleGrid>
      ) : entities.length === 0 ? (
        <Text c="dimmed">No {label.toLowerCase()} yet.</Text>
      ) : (
        <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }}>
          {entities.map(e => (
            <Card
              key={e.id}
              withBorder
              style={{ cursor: 'pointer' }}
              onClick={() => navigate(`/projects/${projectId}/${entityType}/${e.id}`)}
            >
              <Text fw={500}>{e.name}</Text>
              {e.description && (
                <Text size="sm" c="dimmed" lineClamp={2}>
                  <span dangerouslySetInnerHTML={{ __html: e.description }} />
                </Text>
              )}
            </Card>
          ))}
        </SimpleGrid>
      )}
    </Stack>
  );
}
