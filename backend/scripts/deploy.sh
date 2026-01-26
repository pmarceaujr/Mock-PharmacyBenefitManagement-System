#!/bin/bash
set -e

echo "========================================="
echo "PrescriptionTrack Deployment Script"
echo "========================================="
echo ""

# Variables
APP_DIR="/opt/prescriptiontrack"
REPO_URL="https://github.com/yourusername/prescriptiontrack.git"  # Update this

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "1. Updating system..."
apt-get update
apt-get upgrade -y

# Clone or pull repository
if [ -d "$APP_DIR/.git" ]; then
    echo "2. Pulling latest code..."
    cd $APP_DIR
    sudo -u appuser git pull
else
    echo "2. Cloning repository..."
    git clone $REPO_URL $APP_DIR
    chown -R appuser:appuser $APP_DIR
fi

cd $APP_DIR/backend

# Create virtual environment
echo "3. Setting up Python environment..."
if [ ! -d "venv" ]; then
    sudo -u appuser python3.11 -m venv venv
fi

# Install dependencies
echo "4. Installing dependencies..."
sudo -u appuser venv/bin/pip install -r requirements.txt

# Run migrations
echo "5. Running database migrations..."
sudo -u appuser venv/bin/flask db upgrade

# Restart service
echo "6. Restarting application..."
systemctl restart prescriptiontrack
systemctl restart nginx

# Check status
echo "7. Checking service status..."
systemctl status prescriptiontrack --no-pager

echo ""
echo "========================================="
echo "✓ Deployment complete!"
echo "========================================="



