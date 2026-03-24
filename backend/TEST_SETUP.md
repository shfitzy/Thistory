# Backend Test Setup and Execution Guide

## Quick Start

Run these commands to set up and test:

```bash
# 1. Navigate to backend directory
cd backend

# 2. Install dependencies (if not in venv, create one first)
pip3 install -r requirements.txt

# 3. Run tests
python3 -m pytest tests/ -v
```

## Detailed Setup

### Step 1: Install Dependencies

The following new packages are required:
- `pydantic==2.5.0` - Data validation
- `flask-limiter==3.5.0` - Rate limiting
- `python-json-logger==2.0.7` - Structured logging
- `psycopg2-binary==2.9.9` - PostgreSQL driver

Install all dependencies:
```bash
pip3 install -r requirements.txt
```

### Step 2: Verify Installation

Check that key packages are installed:
```bash
python3 -c "import pydantic; print(f'Pydantic: {pydantic.__version__}')"
python3 -c "import flask_limiter; print('Flask-Limiter: OK')"
```

### Step 3: Run Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_models.py -v

# Run with detailed output
python3 -m pytest tests/ -vv --tb=long
```

## Expected Test Results

You should see approximately 20+ tests pass:

**Model Tests** (4 tests):
- ✓ test_user_model_with_is_admin
- ✓ test_project_model_creation
- ✓ test_project_user_relationship
- ✓ test_project_cascade_delete

**CRUD Tests** (8 tests):
- ✓ test_create_project
- ✓ test_get_project
- ✓ test_get_projects_by_user
- ✓ test_get_all_projects_admin
- ✓ test_update_project
- ✓ test_delete_project
- ✓ test_check_project_access
- ✓ test_check_project_modify_access

**API Tests** (10+ tests):
- ✓ test_create_project_api
- ✓ test_list_projects_api
- ✓ test_get_project_api_owner
- ✓ test_get_project_api_unauthorized
- ✓ test_get_public_project_api
- ✓ test_update_project_api
- ✓ test_delete_project_api
- ✓ test_update_visibility_api
- ✓ test_admin_list_all_projects_api
- ✓ test_non_admin_cannot_list_all_projects
- ✓ test_authentication_required

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'pydantic'

**Solution**: Install dependencies
```bash
pip3 install pydantic==2.5.0
# Or install all at once:
pip3 install -r requirements.txt
```

### Issue: Import errors for app modules

**Solution**: Make sure you're in the backend directory
```bash
cd backend
python3 -m pytest tests/ -v
```

### Issue: Database errors

**Solution**: Tests use in-memory SQLite, no setup needed. If errors persist:
```bash
pip3 install --upgrade flask-sqlalchemy
```

## Running Individual Test Categories

```bash
# Only model tests
python3 -m pytest tests/test_models.py -v

# Only CRUD tests
python3 -m pytest tests/test_crud_project.py -v

# Only API tests
python3 -m pytest tests/test_api_projects.py -v
```

## Test Configuration

Tests are configured in:
- `pytest.ini` - Pytest configuration
- `tests/conftest.py` - Test fixtures (app, client, db)
- `app/core/config.py` - TestingConfig class

Tests use:
- In-memory SQLite database (no PostgreSQL required for tests)
- Isolated test database (cleaned between tests)
- Test JWT tokens for authentication
