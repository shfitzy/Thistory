# Backend Testing Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Virtual environment** (recommended)

## Setup

### 1. Create and activate virtual environment (if not already done)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

### Option 1: Using the test runner script (recommended)

```bash
./run_tests.sh
```

### Option 2: Using pytest directly

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::test_user_model_with_is_admin

# Run with coverage report
pytest --cov=app --cov-report=html
```

## Test Structure

```
tests/
├── conftest.py              # Test fixtures and configuration
├── test_models.py           # Model unit tests
├── test_crud_project.py     # CRUD operation tests
└── test_api_projects.py     # API integration tests
```

## Test Coverage

The test suite covers:

- **Model Tests** (test_models.py):
  - User model with is_admin field
  - Project model creation
  - User-Project relationships
  - Cascade delete behavior

- **CRUD Tests** (test_crud_project.py):
  - Create project
  - Get project
  - Get projects by user
  - Get all projects (admin)
  - Update project
  - Delete project
  - Access control checks

- **API Tests** (test_api_projects.py):
  - POST /api/v1/projects (Create project)
  - GET /api/v1/projects (List projects)
  - GET /api/v1/projects/{id} (Get project with access control)
  - PUT /api/v1/projects/{id} (Update project)
  - DELETE /api/v1/projects/{id} (Delete project)
  - PATCH /api/v1/projects/{id}/visibility (Update visibility)
  - GET /api/v1/admin/projects (Admin list all)
  - Authentication and authorization checks

## Troubleshooting

### Import errors

If you see import errors, make sure you're in the backend directory and have activated your virtual environment:

```bash
cd backend
source venv/bin/activate
```

### Database errors

Tests use an in-memory SQLite database, so no setup is required. If you see database errors, ensure SQLAlchemy is properly installed:

```bash
pip install --upgrade flask-sqlalchemy
```

### Missing dependencies

If tests fail due to missing dependencies:

```bash
pip install -r requirements.txt --upgrade
```

## Expected Output

When tests pass, you should see output like:

```
🧪 Running Thistory Backend Tests
==================================

📦 Installing dependencies...

🧪 Running tests...

tests/test_models.py::test_user_model_with_is_admin PASSED
tests/test_models.py::test_project_model_creation PASSED
tests/test_models.py::test_project_user_relationship PASSED
tests/test_models.py::test_project_cascade_delete PASSED
tests/test_crud_project.py::test_create_project PASSED
tests/test_crud_project.py::test_get_project PASSED
...

✅ Tests complete!
```

## Next Steps

After tests pass:
1. Review test coverage
2. Add additional tests as needed
3. Run tests before committing code changes
4. Consider setting up CI/CD to run tests automatically
