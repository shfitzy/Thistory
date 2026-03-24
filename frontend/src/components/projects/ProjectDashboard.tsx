import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { getProject } from '../../api/projects';

export const ProjectDashboard: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const id = parseInt(projectId || '0', 10);

  const { data: project, isLoading, error } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id),
    enabled: id > 0,
  });

  if (isLoading) return <div data-testid="loading">Loading...</div>;
  if (error) return <div data-testid="error">Error loading project</div>;
  if (!project) return <div data-testid="not-found">Project not found</div>;

  return (
    <div className="project-dashboard" data-testid="project-dashboard">
      <header>
        <h1>{project.title}</h1>
        <div className="actions">
          <Link to={`/projects/${project.id}/edit`} data-testid="edit-link">
            Edit
          </Link>
          <Link to={`/projects/${project.id}/settings`} data-testid="settings-link">
            Settings
          </Link>
        </div>
      </header>

      <div className="project-info">
        <p className="short-description">{project.short_description}</p>
        <p className="long-description">{project.long_description}</p>
        <div className="metadata">
          <span className="visibility" data-testid="visibility">
            {project.visibility}
          </span>
          <span className="created" data-testid="created">
            Created: {new Date(project.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      <div className="content-sections">
        <h2>Project Content</h2>
        <div className="content-grid">
          <Link to={`/projects/${project.id}/locations`} className="content-card">
            <h3>Locations</h3>
            <p>Manage places in your world</p>
          </Link>
          <Link to={`/projects/${project.id}/characters`} className="content-card">
            <h3>Characters</h3>
            <p>Manage characters and people</p>
          </Link>
          <Link to={`/projects/${project.id}/events`} className="content-card">
            <h3>Events</h3>
            <p>Manage historical events</p>
          </Link>
          <Link to={`/projects/${project.id}/races`} className="content-card">
            <h3>Races</h3>
            <p>Manage species and races</p>
          </Link>
          <Link to={`/projects/${project.id}/relationships`} className="content-card">
            <h3>Relationships</h3>
            <p>Manage character relationships</p>
          </Link>
        </div>
      </div>
    </div>
  );
};
