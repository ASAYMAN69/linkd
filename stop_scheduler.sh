#!/bin/bash

# Fix potential line ending issues
if [[ "$(printf '%s' "$0" | xxd -p | tail -c 3)" == "0d" ]]; then
    exec tr -d '\r' < "$0" | bash -s "$@"
    exit $?
fi

SERVICE_NAME="linkedin-tracker"
ORCHESTRATOR="orchestrator.py"

echo "🛑 Stopping and removing scheduler..."

# 1. Try removing systemd units
if systemctl --user daemon-reload &>/dev/null; then
    systemctl --user stop "$SERVICE_NAME.timer" 2>/dev/null || true
    systemctl --user disable "$SERVICE_NAME.timer" 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/$SERVICE_NAME.service"
    rm -f "$HOME/.config/systemd/user/$SERVICE_NAME.timer"
    systemctl --user daemon-reload
fi

# 2. Try removing from crontab
(crontab -l 2>/dev/null | grep -v "$ORCHESTRATOR") | crontab - 2>/dev/null || true

echo "✅ All scheduled tasks removed."
