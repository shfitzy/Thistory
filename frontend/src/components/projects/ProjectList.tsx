import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getProjects } from '../../api/projects';

export const ProjectList = () => {
  const { data: projects, isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: getProjects,
  });

  if (isLoading) return <div>Loading projects...</div>;
  if (error) return <div>Error loading projects</div>;

  return (
    <div className="project-list" data-testid="project-list">
      <div className="project-list-header">
        <h2>My Projects</h2>
        <Link to="/projects/new" data-testid="create-project-button">
          <button>Create New Project</button>
        </Link>
      </div>

      {projects && projects.length === 0 ? (
        <p data-testid="no-projects-message">No projects yet. Create your first project!</p>
      ) : (
        <div className="projects-grid">
          {projects?.map((project) => (
            <Link
              key={project.id}
              to={`/projects/${project.id}`}
              className="project-card"
              data-testid={`project-card-${project.id}`}
            >
              <h3>{project.title}</h3>
              <p>{project.short_description}</p>
              <div className="project-meta">
                <span className={`visibility-badge ${project.visibility}`}>
                  {project.visibility}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
