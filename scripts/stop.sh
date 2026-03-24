#!/bin/bash
echo "Stopping Thistory..."

echo ""
echo "Stopping PostgreSQL..."
docker compose down

echo ""
echo "Note: If backend or frontend servers are running in other terminals, close those manually."
echo ""
echo "Done."
