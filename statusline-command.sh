#!/usr/bin/env bash
# Resolve script directory so this works regardless of where it's cloned
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use python3 if available, fall back to python
if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/statusline.py"
else
    python "$SCRIPT_DIR/statusline.py"
fi
