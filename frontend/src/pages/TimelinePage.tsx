import { Container, Title } from '@mantine/core';
import { useParams } from 'react-router-dom';
import { Timeline } from '../components/content/Timeline';

export function TimelinePage() {
  const { projectId } = useParams<{ projectId: string }>();
  const pid = parseInt(projectId ?? '0', 10);

  return (
    <Container size="md" py="xl">
      <Title order={2} mb="lg">Timeline</Title>
      <Timeline projectId={pid} />
    </Container>
  );
}
