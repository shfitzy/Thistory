import React from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { updateProjectVisibility, deleteProject } from '../../api/projects';
import type { Project } from '../../api/projects';

interface ProjectSettingsProps {
  project: Project;
  onClose: () => void;
}

export const ProjectSettings: React.FC<ProjectSettingsProps> = ({ project, onClose }) => {
  const queryClient = useQueryClient();

  const visibilityMutation = useMutation({
    mutationFn: (visibility: 'private' | 'public') =>
      updateProjectVisibility(project.id, visibility),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['project', project.id] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteProject(project.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      onClose();
    },
  });

  const handleVisibilityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    visibilityMutation.mutate(e.target.value as 'private' | 'public');
  };

  const handleDelete = () => {
    if (window.confirm(`Delete project "${project.title}"? This cannot be undone.`)) {
      deleteMutation.mutate();
    }
  };

  return (
    <div className="project-settings" data-testid="project-settings">
      <h3>Project Settings</h3>

      <div className="setting-group">
        <label htmlFor="visibility">Visibility</label>
        <select
          id="visibility"
          value={project.visibility}
          onChange={handleVisibilityChange}
          disabled={visibilityMutation.isPending}
          data-testid="visibility-select"
        >
          <option value="private">Private</option>
          <option value="public">Public</option>
        </select>
        {visibilityMutation.isError && (
          <p className="error" data-testid="visibility-error">
            Failed to update visibility
          </p>
        )}
      </div>

      <div className="setting-group danger-zone">
        <h4>Danger Zone</h4>
        <button
          onClick={handleDelete}
          disabled={deleteMutation.isPending}
          className="btn-danger"
          data-testid="delete-button"
        >
          {deleteMutation.isPending ? 'Deleting...' : 'Delete Project'}
        </button>
        {deleteMutation.isError && (
          <p className="error" data-testid="delete-error">
            Failed to delete project
          </p>
        )}
      </div>

      <button onClick={onClose} data-testid="close-button">
        Close
      </button>
    </div>
  );
};
