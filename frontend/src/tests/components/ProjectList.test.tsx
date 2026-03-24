import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProjectList } from '../../components/projects/ProjectList';
import { getProjects } from '../../api/projects';
import { vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../api/projects');

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
};

describe('ProjectList', () => {
  it('renders loading state', () => {
    vi.mocked(getProjects).mockImplementation(() => new Promise(() => {}));
    render(<ProjectList />, { wrapper: createWrapper() });
    expect(screen.getByText('Loading projects...')).toBeInTheDocument();
  });

  it('renders projects', async () => {
    const projects = [
      { id: 1, title: 'Project 1', short_description: 'Desc 1', long_description: 'Long 1', visibility: 'private' as const, user_id: 1, created_at: '2024-01-01', updated_at: '2024-01-01' },
    ];
    vi.mocked(getProjects).mockResolvedValue(projects);
    
    render(<ProjectList />, { wrapper: createWrapper() });
    
    await waitFor(() => {
      expect(screen.getByText('Project 1')).toBeInTheDocument();
    });
  });
});
