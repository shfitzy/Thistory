import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Container, Group, SimpleGrid, Skeleton, Stack, Text, Title, Badge } from '@mantine/core';
import { IconPlus, IconLogout } from '@tabler/icons-react';
import { useAuth } from '../contexts/AuthContext';
import { getProjects } from '../api/projects';
import type { Project } from '../api/projects';

export const Dashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProjects()
      .then(setProjects)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="xl">
        <Title order={1}>Dashboard</Title>
        <Group>
          <Button
            variant="light"
            leftSection={<IconPlus size={16} />}
            onClick={() => navigate('/projects/new')}
          >
            New Project
          </Button>
          <Button
            variant="subtle"
            color="red"
            leftSection={<IconLogout size={16} />}
            onClick={handleLogout}
          >
            Logout
          </Button>
        </Group>
      </Group>

      <Title order={3} mb="md">Your Projects</Title>

      {loading ? (
        <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }}>
          {[1, 2, 3].map(i => <Skeleton key={i} height={140} radius="md" />)}
        </SimpleGrid>
      ) : projects.length === 0 ? (
        <Card withBorder p="xl" ta="center">
          <Stack align="center" gap="sm">
            <Text c="dimmed" size="lg">No projects yet</Text>
            <Text c="dimmed" size="sm">Create your first worldbuilding project to get started.</Text>
            <Button leftSection={<IconPlus size={16} />} onClick={() => navigate('/projects/new')}>
              Create Project
            </Button>
          </Stack>
        </Card>
      ) : (
        <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }}>
          {projects.map(project => (
            <Card
              key={project.id}
              withBorder
              padding="lg"
              style={{ cursor: 'pointer' }}
              onClick={() => navigate(`/projects/${project.id}`)}
            >
              <Group justify="space-between" mb="xs">
                <Text fw={600} lineClamp={1}>{project.title}</Text>
                <Badge size="sm" variant="light" color={project.visibility === 'public' ? 'green' : 'gray'}>
                  {project.visibility}
                </Badge>
              </Group>
              <Text size="sm" c="dimmed" lineClamp={2} mb="sm">
                {project.short_description}
              </Text>
              <Text size="xs" c="dimmed">
                Created {new Date(project.created_at).toLocaleDateString()}
              </Text>
            </Card>
          ))}
        </SimpleGrid>
      )}
    </Container>
  );
};
