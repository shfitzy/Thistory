import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ProjectForm } from '../components/projects/ProjectForm';
import { getProject } from '../api/projects';

export const EditProjectPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const id = parseInt(projectId || '0', 10);

  const { data: project, isLoading, error } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id),
    enabled: id > 0,
  });

  const handleSuccess = (projectId: number) => {
    navigate(`/projects/${projectId}`);
  };

  const handleCancel = () => {
    navigate(`/projects/${id}`);
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading project</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <div className="edit-project-page">
      <h1>Edit Project</h1>
      <ProjectForm
        project={project}
        mode="edit"
      />
    </div>
  );
};
