# TUI Clock Implementation Plan

## Overview
A terminal-based clock application that displays the current time in Pacific Time (PT) with a secondary display showing Eastern Time (ET).

## Requirements Summary
- Resizable TUI that adapts to terminal window size
- Primary display: Large centered digital clock showing PT time (hh:mm)
- Secondary display: Smaller text below showing ET time (PT + 3 hours)
- Clean execution from fresh venv or via run script
- Blink the terminal screen every 30 minutes

## Technology Stack
- **Language**: Python 3.12
- **TUI Framework**: `textual` - Modern Python TUI framework with excellent resize handling
- **Timezone**: `pytz` for timezone handling

## Task Breakdown

### TASK 1: Project Setup [PRIORITY: HIGH] [STATUS: COMPLETE]
- [x] Create pyproject.toml with dependencies (textual, pytz)
- [x] Create virtual environment
- [x] Install dependencies
- [x] Create basic project structure

**Verification**: ✅ `python3.12 -m pytest` runs successfully, dependencies import correctly

### TASK 2: Basic Clock Implementation [PRIORITY: HIGH] [STATUS: COMPLETE]
- [x] Create main.py with Textual app structure
- [x] Implement time display widget for PT timezone
- [x] Add automatic time updates (every second)
- [x] Center the primary clock display

**Verification**: ✅ Running `python3.12 -m tui_clock.main` shows current PT time updating every second

### TASK 3: Secondary ET Display [PRIORITY: MEDIUM] [STATUS: COMPLETE]
- [x] Add secondary display widget below primary clock
- [x] Calculate and display ET time (using proper ET timezone)
- [x] Style secondary display smaller than primary

**Verification**: ✅ Both PT and ET times display correctly with proper sizing

### TASK 4: Large ASCII Art Font [PRIORITY: MEDIUM] [STATUS: COMPLETE]
- [x] Implement ASCII art digit rendering for primary clock
- [x] Ensure digits scale appropriately with terminal size
- [x] Add colon separator between hours and minutes

**Verification**: ✅ Clock displays with large ASCII art digits that are readable

### TASK 5: Responsive Layout [PRIORITY: MEDIUM] [STATUS: COMPLETE]
- [x] Handle terminal resize events (handled automatically by Textual)
- [x] Adjust font/display size based on terminal dimensions (using auto-sizing)
- [x] Maintain centered layout at all sizes

**Verification**: ✅ Resizing terminal causes clock to adapt smoothly

### TASK 6: Testing & Polish [PRIORITY: LOW] [STATUS: COMPLETE]
- [x] Add unit tests for time calculations
- [x] Add linting configuration (ruff)
- [x] Add type hints throughout
- [ ] Create README.md with usage instructions (deferred - not requested)

**Verification**: ✅ `pytest` passes (5 tests), `ruff check .` passes

### TASK 7: Run Script [PRIORITY: HIGH] [STATUS: COMPLETE]
- [x] Create run.sh script for one-command execution
- [x] Auto-create venv if missing
- [x] Auto-install dependencies if needed

**Verification**: ✅ `./run.sh` launches the application from scratch

### TASK 8: 30-Minute Screen Blink [PRIORITY: HIGH] [STATUS: COMPLETE]
- [x] Add timer to track 30-minute intervals
- [x] Implement screen blink effect (brief color inversion or flash)
- [x] Add unit tests for blink timing logic

**Verification**: ✅ Running the app at :00 or :30 minute mark triggers a visible screen blink (3 quick flashes)

## Progress Log
- Initial plan created
- TASK 1 completed: Project structure with pyproject.toml, venv, dependencies installed
- TASK 2-5 completed: Full TUI clock implementation with:
  - Large ASCII art digits for PT time (7 lines tall)
  - Secondary ET display below
  - Centered layout with Textual CSS
  - Auto-update every second
  - Responsive to terminal resize
- TASK 6 completed: Tests added for digit rendering, ruff linting configured and passing
- TASK 7 completed: Added run.sh script for one-command execution from scratch
- TASK 8 completed: Added 30-minute screen blink feature:
  - Blink triggers at :00 and :30 minute marks
  - Screen flashes 3 times with color inversion (white bg, black text)
  - Unit tests added for blink timing logic (4 new tests, 9 total passing)

## How to Run
```bash
./run.sh
```

Or manually:
```bash
source .venv/bin/activate
python3.12 -m tui_clock.main
```

Press `q` or `Escape` to quit.
