import { useEffect, useState } from 'react';
import { Button, Group, NumberInput, Select, Stack, TextInput } from '@mantine/core';
import { WYSIWYGEditor } from './WYSIWYGEditor';
import type { EntityType } from './CategoryView';
import { listRaces } from '../../api/races';
import type { Race } from '../../api/races';

interface EntityFormProps {
  projectId: number;
  entityType: EntityType;
  initialValues?: Record<string, any>;
  onSubmit: (values: Record<string, any>) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

const CHARACTER_STATUSES = [
  { value: 'alive', label: 'Alive' },
  { value: 'deceased', label: 'Deceased' },
  { value: 'unknown', label: 'Unknown' },
];

export function EntityForm({ projectId, entityType, initialValues = {}, onSubmit, onCancel, loading }: EntityFormProps) {
  const [values, setValues] = useState<Record<string, any>>({ description: '', ...initialValues });
  const [races, setRaces] = useState<Race[]>([]);

  useEffect(() => {
    if (entityType === 'character') {
      listRaces(projectId).then(setRaces).catch(() => {});
    }
  }, [projectId, entityType]);

  const set = (key: string, val: any) => setValues(prev => ({ ...prev, [key]: val }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack>
        <TextInput
          label="Name"
          required
          value={values.name ?? ''}
          onChange={e => set('name', e.target.value)}
        />

        {entityType === 'character' && (
          <>
            <Select
              label="Status"
              data={CHARACTER_STATUSES}
              value={values.status ?? null}
              onChange={val => set('status', val)}
              clearable
            />
            <NumberInput
              label="Age"
              value={values.age ?? ''}
              onChange={val => set('age', val === '' ? undefined : val)}
              min={0}
            />
            <Select
              label="Race"
              data={races.map(r => ({ value: String(r.id), label: r.name }))}
              value={values.race_id != null ? String(values.race_id) : null}
              onChange={val => set('race_id', val ? Number(val) : undefined)}
              clearable
              searchable
            />
          </>
        )}

        {entityType === 'event' && (
          <>
            <TextInput
              label="Event Date"
              required
              placeholder="e.g. Year 342, Age of Fire"
              value={values.event_date ?? ''}
              onChange={e => set('event_date', e.target.value)}
            />
            <TextInput
              label="Event End Date"
              placeholder="Optional"
              value={values.event_date_end ?? ''}
              onChange={e => set('event_date_end', e.target.value || undefined)}
            />
          </>
        )}

        <div>
          <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 4 }}>Description</div>
          <WYSIWYGEditor value={values.description ?? ''} onChange={val => set('description', val)} />
        </div>

        <Group justify="flex-end">
          <Button variant="subtle" onClick={onCancel} disabled={loading}>Cancel</Button>
          <Button type="submit" loading={loading}>Save</Button>
        </Group>
      </Stack>
    </form>
  );
}
