# THistory Backend API

A RESTful API backend built with Flask, Flask-RESTX, SQLAlchemy, and JWT authentication.

## Features

- Flask framework with Flask-RESTX for API structure
- Automatic Swagger/OpenAPI documentation
- JWT-based authentication with Flask-JWT-Extended
- SQLAlchemy ORM with Alembic migrations
- User management (CRUD operations)
- CORS support for frontend integration

## Setup

### Prerequisites

- Python 3.8+ (check with `python3 --version`)
- pip (usually comes with Python, check with `python3 -m pip --version`)

### Installation

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
# Use python3 -m pip if 'pip' command is not found
python3 -m pip install -r requirements.txt

# Or if pip3 is available:
pip3 install -r requirements.txt
```

3. Create a `.env` file in the `backend` directory:

```bash
# Database
DATABASE_URL=sqlite:///app.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-secret-key-here-change-in-production

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

4. Initialize the database:

```bash
flask db init  # Only needed once
flask db migrate -m "Initial migration"
flask db upgrade
```

Or using Alembic directly:

```bash
alembic upgrade head
```

## Running the Server

```bash
python3 -m app.main
```

Or using Flask CLI:

```bash
export FLASK_APP=app.main
flask run
```

## Troubleshooting

### "pip: command not found"

On macOS/Linux, use `python3 -m pip` instead of `pip`:

```bash
python3 -m pip install -r requirements.txt
```

Alternatively, you can use `pip3` if it's available:

```bash
pip3 install -r requirements.txt
```

### "python: command not found"

Use `python3` instead of `python`:

```bash
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

The API will be available at `http://localhost:5000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:5000/docs/

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users (Protected)

- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-token>
```

To get a token, use the `/api/v1/auth/login` endpoint:

```json
{
  "username": "your_username_or_email",
  "password": "your_password"
}
```

## Database Migrations

Using Flask-Migrate (recommended):

```bash
flask db migrate -m "description"
flask db upgrade
flask db downgrade
```

Or using Alembic directly:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes (Flask-RESTX namespaces)
│   ├── core/          # Core functionality (security, config)
│   ├── crud/          # Database operations
│   ├── models/        # SQLAlchemy models
│   ├── database.py    # Database connection (Flask-SQLAlchemy)
│   └── main.py        # Flask app
├── alembic/           # Database migrations
├── tests/             # Test files
└── requirements.txt    # Python dependencies
```
