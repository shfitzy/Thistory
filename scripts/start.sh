#!/bin/bash
echo "Starting Thistory..."

echo ""
echo "Starting PostgreSQL via Docker..."
docker compose up -d
docker compose ps

echo ""
echo "Docker is running. Start the following in separate terminal tabs:"
echo ""
echo "  Backend:  cd backend && source venv/bin/activate && python3 -m app.main"
echo "  Frontend: cd frontend && nvm use && npm run dev"
echo ""
echo "App will be available at http://localhost:5173"
