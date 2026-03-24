import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { AdminDashboard } from '../../components/admin/AdminDashboard';
import { getAllProjects } from '../../api/projects';
import { vi } from 'vitest';

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

describe('AdminDashboard', () => {
  it('renders all projects for admin', async () => {
    const projects = [
      { id: 1, title: 'Project 1', short_description: 'Desc 1', long_description: 'Long 1', visibility: 'private', user_id: 1, created_at: '2024-01-01', updated_at: '2024-01-01' },
      { id: 2, title: 'Project 2', short_description: 'Desc 2', long_description: 'Long 2', visibility: 'public', user_id: 2, created_at: '2024-01-02', updated_at: '2024-01-02' },
    ];
    vi.mocked(getAllProjects).mockResolvedValue(projects);
    
    render(<AdminDashboard />, { wrapper: createWrapper() });
    
    await waitFor(() => {
      expect(screen.getByText('Project 1')).toBeInTheDocument();
      expect(screen.getByText('Project 2')).toBeInTheDocument();
    });
  });
});
