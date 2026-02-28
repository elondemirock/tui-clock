# Agent Operational Guide

## Commands

```bash
# Activate virtual environment (required before running commands)
source .venv/bin/activate

# Run tests
python -m pytest tests/ -v

# Run linting
python -m ruff check .

# Run the application
python -m tui_clock.main
# or after pip install -e .
tui-clock
```

## Project Structure

- `tui_clock/` - Main source code
- `tests/` - Test files
- `specs/` - Feature specifications
- `.water_stats` - Runtime water tracking data (JSON)
- Config files: `.tui_clock.toml` (local) or `~/.config/tui-clock/config.toml` (XDG)
