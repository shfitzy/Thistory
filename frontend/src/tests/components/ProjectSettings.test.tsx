import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProjectSettings } from '../../components/projects/ProjectSettings';
import { updateProjectVisibility, deleteProject } from '../../api/projects';
import { vi } from 'vitest';

vi.mock('../../api/projects');

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

const mockProject = {
  id: 1,
  title: 'Test Project',
  short_description: 'Desc',
  long_description: 'Long',
  visibility: 'private' as const,
  user_id: 1,
  created_at: '2024-01-01',
  updated_at: '2024-01-01',
};

describe('ProjectSettings', () => {
  it('updates visibility', async () => {
    vi.mocked(updateProjectVisibility).mockResolvedValue({ ...mockProject, visibility: 'public' });
    const onClose = vi.fn();
    
    render(<ProjectSettings project={mockProject} onClose={onClose} />, { wrapper: createWrapper() });
    
    fireEvent.change(screen.getByTestId('visibility-select'), { target: { value: 'public' } });
    
    await waitFor(() => {
      expect(updateProjectVisibility).toHaveBeenCalledWith(1, 'public');
    });
  });

  it('deletes project with confirmation', async () => {
    vi.mocked(deleteProject).mockResolvedValue(undefined);
    const onClose = vi.fn();
    window.confirm = vi.fn(() => true);
    
    render(<ProjectSettings project={mockProject} onClose={onClose} />, { wrapper: createWrapper() });
    
    fireEvent.click(screen.getByTestId('delete-button'));
    
    await waitFor(() => {
      expect(deleteProject).toHaveBeenCalledWith(1);
      expect(onClose).toHaveBeenCalled();
    });
  });
});
