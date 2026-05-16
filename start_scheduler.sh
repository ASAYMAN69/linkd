#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR=$(pwd)
SERVICE_NAME="linkedin-tracker"
SERVICE_FILE="$HOME/.config/systemd/user/$SERVICE_NAME.service"
TIMER_FILE="$HOME/.config/systemd/user/$SERVICE_NAME.timer"

echo "⏲️ Setting up automated scheduler (9 AM daily)..."

# Create systemd user directory if it doesn't exist
mkdir -p "$HOME/.config/systemd/user"

# Create the service file
cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=LinkedIn Activity Tracker Service
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python3 $PROJECT_DIR/orchestrator.py
StandardOutput=append:$PROJECT_DIR/scheduler.log
StandardError=append:$PROJECT_DIR/scheduler.log

[Install]
WantedBy=default.target
EOF

# Create the timer file
cat <<EOF > "$TIMER_FILE"
[Unit]
Description=Run LinkedIn Activity Tracker daily at 9 AM

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true
Unit=$SERVICE_NAME.service

[Install]
WantedBy=timers.target
EOF

# Reload systemd user daemon
systemctl --user daemon-reload

# Enable and start the timer
systemctl --user enable "$SERVICE_NAME.timer"
systemctl --user start "$SERVICE_NAME.timer"

# Fire right now as requested
echo "🚀 Triggering initial run..."
systemctl --user start "$SERVICE_NAME.service"

echo ""
echo "✅ Scheduler is active!"
echo "📍 Task will run every day at 9:00 AM."
echo "📍 If the device is off at 9:00 AM, it will run immediately when turned on."
echo "📍 Logs are available at: $PROJECT_DIR/scheduler.log"
echo "📍 To disable, run: ./stop_scheduler.sh"
