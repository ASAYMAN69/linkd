#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Scrapling LinkedIn Tracker..."

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

# Upgrade pip and install Scrapling in editable mode with fetchers
echo "🛠 Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -e "./Scrapling[fetchers]"

# Install Playwright/Patchright browsers
echo "🌐 Installing Chromium browsers..."
./venv/bin/python3 -m playwright install chromium
./venv/bin/python3 -m patchright install chromium

echo ""
echo "✨ Setup Complete!"
echo "===================================================="
echo "1. Run manual login to LinkedIn (ONE TIME):"
echo "   ./venv/bin/python3 open_browser.py"
echo ""
echo "2. Run the tracker:"
echo "   ./venv/bin/python3 linkedin_tracker.py <profile_url>"
echo "===================================================="
