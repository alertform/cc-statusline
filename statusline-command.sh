#!/usr/bin/env bash
# Resolve script directory so this works regardless of where it's cloned
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use python3 if available, fall back to python
if python3 -c "import sys; sys.exit(0)" &>/dev/null 2>&1; then
    python3 "$SCRIPT_DIR/statusline.py"
elif command -v python &>/dev/null; then
    python "$SCRIPT_DIR/statusline.py"
fi
