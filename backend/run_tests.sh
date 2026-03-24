#!/bin/bash

# Backend Test Runner Script

echo "🧪 Running Thistory Backend Tests"
echo "=================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating your venv first:"
    echo "   source venv/bin/activate"
    echo ""
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🧪 Running tests..."
echo ""

# Run pytest with coverage
pytest tests/ -v --tb=short

echo ""
echo "✅ Tests complete!"
