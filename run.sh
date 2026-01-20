#!/bin/bash
# Run the TUI Clock application
# Creates a virtual environment if needed and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies if needed
if ! python3.12 -c "import textual, pytz" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -e . --quiet
fi

# Run the application
python3.12 -m tui_clock.main
