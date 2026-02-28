# Implementation Plan: Water Record & Streak Counter

Based on analysis of `specs/default.md` vs. current implementation in `tui_clock/main.py`.

## Summary

The spec requires adding optional tracking for water consumption achievements:
- **Daily record**: Highest single-day drink count from `.water_stats` history
- **Streak**: Consecutive days meeting a configurable daily goal
- Both features must be opt-in (disabled by default)

## Items to Implement (Priority Order)

### P1: Configuration File Support ✅ COMPLETED

- [x] Create config file loader (`~/.config/tui-clock/config.toml` or `.tui_clock.toml` in project root)
- [x] Define config schema with:
  - `daily_goal: int | None` (required if goal tracking enabled)
  - `show_goal: bool` (default: false)
  - `show_streak: bool` (default: false)
  - `show_record: bool` (default: false)
- [x] Load config on app startup in `TuiClockApp.__init__`
- [x] Add tests for config loading, defaults, and missing file handling

**Implementation Details:**
- Created `tui_clock/config.py` with `Config` dataclass and `load_config()` function
- Uses Python 3.11+ built-in `tomllib` (no external dependency needed)
- Config paths searched in order: `.tui_clock.toml` (local), `~/.config/tui-clock/config.toml` (XDG)
- Config is frozen (immutable) dataclass
- Gracefully handles missing files and invalid TOML
- `TuiClockApp.__init__` accepts optional `Config` parameter for testability
- 15 tests in `tests/test_config.py` covering all scenarios

### P2: Daily Goal Display ("x/y" Format) ✅ COMPLETED
- [x] Modify `WaterCounter.update_count()` to accept optional `goal` parameter
- [x] When `show_goal` is enabled, display `💧 {count}/{goal}` instead of `💧 {count}`
- [x] Update all call sites: `on_mount`, `on_click`, `_check_water`
- [x] Add tests for goal display format

**Implementation Details:**
- Modified `WaterCounter.update_count(count, goal=None)` to accept optional goal parameter
- Added `TuiClockApp._get_display_goal()` helper that returns goal when both `show_goal=True` AND `daily_goal` is set
- Updated all 3 call sites (`on_mount`, `on_click`, `_check_water`) to pass goal parameter
- Added 8 tests in `tests/test_water.py` covering:
  - `_get_display_goal()` behavior with various config combinations
  - Format string logic for count-only and count/goal display

### P3: Daily Record Calculation
- [ ] Add function `calculate_daily_record(history: dict, today_count: int) -> int`
  - Compute max of all historical counts + today's count
  - History is already stored in `.water_stats["history"]` as `{date: count}`
- [ ] No new persistence needed (computed from existing data)
- [ ] Add tests for record calculation (empty history, single day, multiple days)

### P4: Streak Calculation
- [ ] Add function `calculate_streak(history: dict, today: str, today_count: int, goal: int) -> int`
  - Count consecutive days (ending today or yesterday) where count >= goal
  - Must handle gaps in dates (non-consecutive dates break streak)
- [ ] Add tests for streak logic:
  - No streak when today below goal
  - Streak continues from yesterday
  - Gaps break streak
  - Streak includes today if today >= goal

### P5: Water Stats Popup
- [ ] Create `WaterStatsPopup` widget (or modal overlay)
- [ ] Display on interaction (click on WaterCounter, or separate keybinding?)
- [ ] Layout:
  ```
  💧 {count}/{goal}     (or just 💧 {count} if goal disabled)
  🔥 {streak} days      (if show_streak enabled)
  🏆 {record}           (if show_record enabled)
  ```
- [ ] Style popup consistently with existing app theme
- [ ] Dismiss popup on click outside or key press
- [ ] Add tests for popup visibility and content

### P6: Integration & Polish
- [ ] Wire config to app startup
- [ ] Update `_check_water` and `on_click` to refresh streak/record displays
- [ ] Ensure streak/record update when day changes at midnight
- [ ] Add example config file to README or create `.tui_clock.toml.example`

## Notes

- **Existing infrastructure**: History is already persisted in `.water_stats["history"]` as `{date: count}` pairs. The daily record and streak can be computed from this without new storage.
- **No breaking changes**: Features are opt-in with default `false`, preserving existing behavior.
- **Testing**: Each feature should have unit tests. Consider using freezegun or manual mocking for date-dependent logic.
- **No external TOML dependency**: Python 3.11+ includes `tomllib` in stdlib, so no new dependency needed.

## Files Modified

- `tui_clock/config.py` - NEW: Config loading module
- `tui_clock/main.py` - Added config import and loading in `TuiClockApp.__init__`; P2: added `_get_display_goal()` helper and updated `WaterCounter.update_count()` with optional goal parameter
- `tests/test_config.py` - NEW: Config tests (15 tests)
- `tests/test_water.py` - NEW: Water counter and goal display tests (8 tests)
