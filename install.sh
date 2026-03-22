#!/usr/bin/env bash
# install.sh — sets up cc-statusline for Claude Code

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETTINGS="$HOME/.claude/settings.json"

echo "Installing cc-statusline from $REPO_DIR..."

# Update settings.json to point to this repo's script
if [ -f "$SETTINGS" ]; then
    # Replace the statusLine command in settings.json
    if command -v python3 &>/dev/null; then
        python3 - <<EOF
import json, sys

with open('$SETTINGS', 'r') as f:
    cfg = json.load(f)

cfg.setdefault('statusLine', {})['command'] = 'bash $REPO_DIR/statusline-command.sh'

with open('$SETTINGS', 'w') as f:
    json.dump(cfg, f, indent=2)

print('Updated settings.json')
EOF
    else
        echo "python3 not found — manually set in $SETTINGS:"
        echo "  \"statusLine\": { \"command\": \"bash $REPO_DIR/statusline-command.sh\" }"
    fi
else
    echo "settings.json not found at $SETTINGS"
    echo "Manually add: \"statusLine\": { \"command\": \"bash $REPO_DIR/statusline-command.sh\" }"
fi

echo "Done! Restart Claude Code to apply changes."
