#!/bin/bash

# Initialize migrations directory (first time only)
if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    flask db init
fi

# Create migration
echo "Creating migration..."
flask db migrate -m "Initial migration"

# Apply migration
echo "Applying migration..."
flask db upgrade

echo "✓ Migrations complete!"
