#!/bin/bash
set -e

echo "========================================="
echo "Running Local Tests"
echo "========================================="
echo ""

cd backend

# Activate virtual environment
source venv/bin/activate

# Run linting
echo "1. Running flake8..."
flake8 app --max-line-length=120 || true

# Run tests
echo ""
echo "2. Running pytest..."
pytest

# Generate coverage report
echo ""
echo "3. Coverage report generated in htmlcov/"
echo "   Open htmlcov/index.html in your browser"

echo ""
echo "========================================="
echo "✓ Tests complete!"
echo "========================================="
