import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getAllProjects } from '../../api/projects';

export const AdminDashboard: React.FC = () => {
  const { data: projects, isLoading, error } = useQuery({
    queryKey: ['admin', 'projects'],
    queryFn: getAllProjects,
  });

  if (isLoading) return <div data-testid="loading">Loading...</div>;
  if (error) return <div data-testid="error">Error loading projects</div>;

  return (
    <div className="admin-dashboard" data-testid="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <h2>All Projects ({projects?.length || 0})</h2>

      <table data-testid="projects-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Owner ID</th>
            <th>Visibility</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {projects?.map((project) => (
            <tr key={project.id} data-testid={`project-row-${project.id}`}>
              <td>{project.id}</td>
              <td>{project.title}</td>
              <td>{project.user_id}</td>
              <td>{project.visibility}</td>
              <td>{new Date(project.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {projects?.length === 0 && (
        <p data-testid="no-projects">No projects found</p>
      )}
    </div>
  );
};
