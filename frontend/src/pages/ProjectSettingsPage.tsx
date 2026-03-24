import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ProjectSettings } from '../components/projects/ProjectSettings';
import { getProject } from '../api/projects';

export const ProjectSettingsPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const id = parseInt(projectId || '0', 10);

  const { data: project, isLoading, error } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id),
    enabled: id > 0,
  });

  const handleClose = () => {
    navigate(`/projects/${id}`);
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading project</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <div className="project-settings-page">
      <ProjectSettings project={project} onClose={handleClose} />
    </div>
  );
};
