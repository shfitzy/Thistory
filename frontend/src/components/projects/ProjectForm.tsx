import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { createProject, updateProject } from '../../api/projects';
import type { Project, ProjectCreate, ProjectUpdate } from '../../api/projects';

interface ProjectFormProps {
  project?: Project;
  mode: 'create' | 'edit';
}

export const ProjectForm = ({ project, mode }: ProjectFormProps) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    title: project?.title || '',
    short_description: project?.short_description || '',
    long_description: project?.long_description || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const createMutation = useMutation({
    mutationFn: (data: ProjectCreate) => createProject(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      navigate(`/projects/${data.id}`);
    },
    onError: (error: any) => {
      setErrors({ submit: error.response?.data?.details || 'Failed to create project' });
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: ProjectUpdate) => updateProject(project!.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['project', project!.id] });
      navigate(`/projects/${project!.id}`);
    },
    onError: (error: any) => {
      setErrors({ submit: error.response?.data?.details || 'Failed to update project' });
    },
  });

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (!formData.short_description.trim()) {
      newErrors.short_description = 'Short description is required';
    } else if (formData.short_description.length > 500) {
      newErrors.short_description = 'Short description must be 500 characters or less';
    }

    if (!formData.long_description.trim()) {
      newErrors.long_description = 'Long description is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    if (mode === 'create') {
      createMutation.mutate(formData);
    } else {
      updateMutation.mutate(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="project-form" data-testid="project-form">
      <h2>{mode === 'create' ? 'Create New Project' : 'Edit Project'}</h2>

      {errors.submit && (
        <div className="error-message" data-testid="form-error">
          {errors.submit}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          data-testid="project-form-title-input"
          maxLength={200}
        />
        {errors.title && <span className="field-error">{errors.title}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="short_description">Short Description *</label>
        <textarea
          id="short_description"
          value={formData.short_description}
          onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
          data-testid="project-form-short-description-input"
          maxLength={500}
          rows={3}
        />
        {errors.short_description && <span className="field-error">{errors.short_description}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="long_description">Long Description *</label>
        <textarea
          id="long_description"
          value={formData.long_description}
          onChange={(e) => setFormData({ ...formData, long_description: e.target.value })}
          data-testid="project-form-long-description-input"
          rows={10}
        />
        {errors.long_description && <span className="field-error">{errors.long_description}</span>}
      </div>

      <div className="form-actions">
        <button
          type="submit"
          disabled={createMutation.isPending || updateMutation.isPending}
          data-testid="project-form-submit-button"
        >
          {mode === 'create' ? 'Create Project' : 'Save Changes'}
        </button>
        <button
          type="button"
          onClick={() => navigate(-1)}
          data-testid="project-form-cancel-button"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};
