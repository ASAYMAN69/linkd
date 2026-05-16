#!/bin/bash

# =================================================================
# ROBUST LINKEDIN TRACKER SCHEDULER
# Works on most Linux distros, WSL, and different mount types.
# =================================================================

# 1. Fix potential line ending issues (CRLF from Windows)
# If this script was pulled on Windows, we'll fix it in memory
if [[ "$(printf '%s' "$0" | xxd -p | tail -c 3)" == "0d" ]]; then
    exec tr -d '\r' < "$0" | bash -s "$@"
    exit $?
fi

set -e

# 2. Get absolute paths (Works even if called from outside the folder)
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
ORCHESTRATOR="$SCRIPT_DIR/orchestrator.py"
LOG_FILE="$SCRIPT_DIR/scheduler.log"

echo "🔍 Detecting environment..."
echo "📍 Project directory: $SCRIPT_DIR"

# Check if venv exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ Error: Virtual environment not found at $PYTHON_BIN"
    echo "Please run ./setup.sh first."
    exit 1
fi

# 3. Detect Scheduler Type (Systemd vs Cron)
# Systemd is preferred for its "Persistent=true" (catch-up) feature.
if systemctl --user daemon-reload &>/dev/null; then
    SCHEDULER="systemd"
    echo "✅ Systemd detected. Using persistent timer (best for catch-up)."
else
    SCHEDULER="cron"
    echo "⚠️ Systemd user mode not available. Falling back to Crontab."
fi

if [ "$SCHEDULER" == "systemd" ]; then
    SERVICE_NAME="linkedin-tracker"
    SERVICE_FILE="$HOME/.config/systemd/user/$SERVICE_NAME.service"
    TIMER_FILE="$HOME/.config/systemd/user/$SERVICE_NAME.timer"

    mkdir -p "$HOME/.config/systemd/user"

    # Create Service
    cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=LinkedIn Activity Tracker Service
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$SCRIPT_DIR
ExecStart=$PYTHON_BIN $ORCHESTRATOR
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=default.target
EOF

    # Create Timer with Persistence
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

    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME.timer"
    systemctl --user start "$SERVICE_NAME.timer"
    echo "🚀 Triggering initial run via systemd..."
    systemctl --user start "$SERVICE_NAME.service"

else
    # CRON FALLBACK
    # We use a trick to emulate "Persistent" by checking if we ran today
    # But for simplicity, we'll just set a standard 9 AM cron
    (crontab -l 2>/dev/null | grep -v "$ORCHESTRATOR" ; echo "0 9 * * * $PYTHON_BIN $ORCHESTRATOR >> $LOG_FILE 2>&1") | crontab -
    
    echo "🚀 Triggering initial run manually..."
    $PYTHON_BIN $ORCHESTRATOR >> $LOG_FILE 2>&1 &
fi

echo ""
echo "✨ Scheduler Ready!"
echo "📍 Scheduled for: Daily at 9:00 AM"
echo "📍 Logs: $LOG_FILE"
echo ""
echo "💡 Note: If you are on a restricted mount (like NTFS/Shared Drive),"
echo "   always run this script with: bash start_scheduler.sh"
