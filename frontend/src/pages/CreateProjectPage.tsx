import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ProjectForm } from '../components/projects/ProjectForm';

export const CreateProjectPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSuccess = (projectId: number) => {
    navigate(`/projects/${projectId}`);
  };

  const handleCancel = () => {
    navigate('/projects');
  };

  return (
    <div className="create-project-page">
      <h1>Create New Project</h1>
      <ProjectForm mode="create" />
    </div>
  );
};
