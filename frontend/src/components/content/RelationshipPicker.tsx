import { useEffect, useState } from 'react';
import { Button, Group, Select, Stack, TextInput } from '@mantine/core';
import { listLocations } from '../../api/locations';
import { listRaces } from '../../api/races';
import { listCharacters } from '../../api/characters';
import { listEvents } from '../../api/events';
import { createRelationship } from '../../api/relationships';

type EntityType = 'location' | 'race' | 'character' | 'event';

const ENTITY_TYPES: { value: EntityType; label: string }[] = [
  { value: 'location', label: 'Location' },
  { value: 'race', label: 'Race' },
  { value: 'character', label: 'Character' },
  { value: 'event', label: 'Event' },
];

interface RelationshipPickerProps {
  projectId: number;
  fromEntityType: EntityType;
  fromEntityId: number;
  onCreated: () => void;
}

export function RelationshipPicker({ projectId, fromEntityType, fromEntityId, onCreated }: RelationshipPickerProps) {
  const [toType, setToType] = useState<EntityType | null>(null);
  const [toId, setToId] = useState<string | null>(null);
  const [relType, setRelType] = useState('');
  const [entities, setEntities] = useState<{ value: string; label: string }[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!toType) return;
    const fetchers: Record<EntityType, () => Promise<{ id: number; name: string }[]>> = {
      location: () => listLocations(projectId),
      race: () => listRaces(projectId),
      character: () => listCharacters(projectId),
      event: () => listEvents(projectId),
    };
    fetchers[toType]().then(items =>
      setEntities(items.map(i => ({ value: String(i.id), label: i.name })))
    ).catch(() => {});
    setToId(null);
  }, [toType, projectId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!toType || !toId) return;
    setLoading(true);
    try {
      await createRelationship(projectId, {
        from_entity_type: fromEntityType,
        from_entity_id: fromEntityId,
        to_entity_type: toType,
        to_entity_id: Number(toId),
        relationship_type: relType || undefined,
      });
      setToType(null);
      setToId(null);
      setRelType('');
      onCreated();
    } catch {
      // error handled by caller
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack gap="sm">
        <Group align="flex-end">
          <Select
            label="Entity Type"
            data={ENTITY_TYPES}
            value={toType}
            onChange={val => setToType(val as EntityType)}
            style={{ flex: 1 }}
          />
          <Select
            label="Entity"
            data={entities}
            value={toId}
            onChange={setToId}
            disabled={!toType}
            searchable
            style={{ flex: 2 }}
          />
          <TextInput
            label="Relationship Type"
            placeholder="e.g. ally, enemy"
            value={relType}
            onChange={e => setRelType(e.target.value)}
            style={{ flex: 2 }}
          />
          <Button type="submit" loading={loading} disabled={!toType || !toId}>
            Add
          </Button>
        </Group>
      </Stack>
    </form>
  );
}
