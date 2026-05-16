#!/bin/bash

SERVICE_NAME="linkedin-tracker"

echo "🛑 Stopping and removing automated scheduler..."

# Stop and disable the timer and service
systemctl --user stop "$SERVICE_NAME.timer" 2>/dev/null || true
systemctl --user disable "$SERVICE_NAME.timer" 2>/dev/null || true
systemctl --user stop "$SERVICE_NAME.service" 2>/dev/null || true

# Remove the files
rm -f "$HOME/.config/systemd/user/$SERVICE_NAME.service"
rm -f "$HOME/.config/systemd/user/$SERVICE_NAME.timer"

# Reload systemd user daemon
systemctl --user daemon-reload

echo "✅ Scheduler removed successfully."
