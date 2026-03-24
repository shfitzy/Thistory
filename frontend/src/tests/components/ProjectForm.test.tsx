import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ProjectForm } from '../../components/projects/ProjectForm';
import { createProject, updateProject } from '../../api/projects';
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

describe('ProjectForm', () => {
  it('validates required fields', async () => {
    render(<ProjectForm mode="create" />, { wrapper: createWrapper() });
    
    fireEvent.click(screen.getByTestId('project-form-submit-button'));
    
    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
    });
  });

  it('creates project successfully', async () => {
    vi.mocked(createProject).mockResolvedValue({ id: 1, title: 'Test', short_description: 'Desc', long_description: 'Long', visibility: 'private', user_id: 1, created_at: '2024-01-01', updated_at: '2024-01-01' });
    
    render(<ProjectForm mode="create" />, { wrapper: createWrapper() });
    
    fireEvent.change(screen.getByTestId('project-form-title-input'), { target: { value: 'Test Project' } });
    fireEvent.change(screen.getByTestId('project-form-short-description-input'), { target: { value: 'Short desc' } });
    fireEvent.change(screen.getByTestId('project-form-long-description-input'), { target: { value: 'Long desc' } });
    fireEvent.click(screen.getByTestId('project-form-submit-button'));
    
    await waitFor(() => {
      expect(createProject).toHaveBeenCalled();
    });
  });
});
