import { useEffect, useState } from 'react';
import { ActionIcon, Badge, Button, Group, Paper, Stack, Text, Title } from '@mantine/core';
import { IconEdit, IconTrash, IconX } from '@tabler/icons-react';
import { listRelationships, deleteRelationship } from '../../api/relationships';
import type { Relationship } from '../../api/relationships';
import { RelationshipPicker } from './RelationshipPicker';

type EntityType = 'location' | 'race' | 'character' | 'event';

interface EntityDetailProps {
  projectId: number;
  entityType: EntityType;
  entity: Record<string, any>;
  onEdit: () => void;
  onDelete: () => void;
}

export function EntityDetail({ projectId, entityType, entity, onEdit, onDelete }: EntityDetailProps) {
  const [relationships, setRelationships] = useState<Relationship[]>([]);

  const loadRelationships = () => {
    listRelationships(projectId, entityType, entity.id)
      .then(setRelationships)
      .catch(() => {});
  };

  useEffect(() => { loadRelationships(); }, [projectId, entityType, entity.id]);

  const handleDeleteRelationship = async (id: number) => {
    await deleteRelationship(projectId, id);
    loadRelationships();
  };

  return (
    <Stack>
      <Group justify="space-between">
        <Title order={2}>{entity.name}</Title>
        <Group>
          <Button leftSection={<IconEdit size={16} />} variant="light" onClick={onEdit}>Edit</Button>
          <Button leftSection={<IconTrash size={16} />} variant="light" color="red" onClick={onDelete}>Delete</Button>
        </Group>
      </Group>

      {/* Entity-specific fields */}
      {entityType === 'character' && (
        <Group>
          {entity.status && <Badge>{entity.status}</Badge>}
          {entity.age != null && <Text size="sm">Age: {entity.age}</Text>}
        </Group>
      )}
      {entityType === 'event' && (
        <Text size="sm" c="dimmed">
          {entity.event_date}{entity.event_date_end ? ` — ${entity.event_date_end}` : ''}
        </Text>
      )}

      {/* Description */}
      {entity.description && (
        <Paper withBorder p="md">
          <div dangerouslySetInnerHTML={{ __html: entity.description }} />
        </Paper>
      )}

      {/* Relationships */}
      <Stack gap="xs">
        <Title order={4}>Relationships</Title>
        {relationships.length === 0 && <Text size="sm" c="dimmed">No relationships yet.</Text>}
        {relationships.map(r => {
          const isFrom = r.from_entity_type === entityType && r.from_entity_id === entity.id;
          const otherType = isFrom ? r.to_entity_type : r.from_entity_type;
          const otherId = isFrom ? r.to_entity_id : r.from_entity_id;
          return (
            <Group key={r.id} justify="space-between">
              <Text size="sm">
                {r.relationship_type && <Badge mr="xs" variant="outline">{r.relationship_type}</Badge>}
                {otherType} #{otherId}
              </Text>
              <ActionIcon
                variant="subtle"
                color="red"
                size="sm"
                onClick={() => handleDeleteRelationship(r.id)}
                aria-label="Remove relationship"
              >
                <IconX size={14} />
              </ActionIcon>
            </Group>
          );
        })}
        <RelationshipPicker
          projectId={projectId}
          fromEntityType={entityType}
          fromEntityId={entity.id}
          onCreated={loadRelationships}
        />
      </Stack>
    </Stack>
  );
}
