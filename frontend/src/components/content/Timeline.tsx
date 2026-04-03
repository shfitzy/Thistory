import { useEffect, useState } from 'react';
import { Card, Skeleton, Stack, Text, Title } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { listEvents } from '../../api/events';
import type { Event } from '../../api/events';

interface TimelineProps {
  projectId: number;
}

export function Timeline({ projectId }: TimelineProps) {
  const navigate = useNavigate();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listEvents(projectId)
      .then(data => {
        // Sort by event_date string — works for consistent date formats
        const sorted = [...data].sort((a, b) =>
          (a.event_date ?? '').localeCompare(b.event_date ?? '')
        );
        setEvents(sorted);
      })
      .finally(() => setLoading(false));
  }, [projectId]);

  if (loading) return <Stack>{[1, 2, 3].map(i => <Skeleton key={i} height={60} />)}</Stack>;

  if (events.length === 0) return <Text c="dimmed">No events yet.</Text>;

  return (
    <Stack>
      {events.map(event => (
        <Card
          key={event.id}
          withBorder
          style={{ cursor: 'pointer', borderLeft: '3px solid var(--mantine-color-blue-5)' }}
          onClick={() => navigate(`/projects/${projectId}/events/${event.id}`)}
        >
          <Text fw={500}>{event.name}</Text>
          <Text size="sm" c="dimmed">
            {event.event_date}{event.event_date_end ? ` — ${event.event_date_end}` : ''}
          </Text>
        </Card>
      ))}
    </Stack>
  );
}
