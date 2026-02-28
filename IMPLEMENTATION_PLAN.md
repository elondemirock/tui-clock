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

### P3: Daily Record Calculation ✅ COMPLETED
- [x] Add function `calculate_daily_record(history: dict, today_count: int) -> int`
  - Compute max of all historical counts + today's count
  - History is already stored in `.water_stats["history"]` as `{date: count}`
- [x] No new persistence needed (computed from existing data)
- [x] Add tests for record calculation (empty history, single day, multiple days)

**Implementation Details:**
- Added `calculate_daily_record(history: dict, today_count: int) -> int` function in `tui_clock/main.py:104-116`
- Returns today_count if history is empty, otherwise returns max of historical values and today_count
- Added 7 tests in `tests/test_water.py` class `TestCalculateDailyRecord`:
  - `test_empty_history_returns_today_count` - empty history returns today's count
  - `test_empty_history_with_zero_today` - empty history with zero returns 0
  - `test_single_day_history_higher_than_today` - historical record higher than today
  - `test_single_day_history_lower_than_today` - today beats historical record
  - `test_multiple_days_history` - finds max across multiple days
  - `test_today_beats_all_history` - today is new record
  - `test_today_equals_historical_max` - today ties with historical record

### P4: Streak Calculation ✅ COMPLETED
- [x] Add function `calculate_streak(history: dict, today: str, today_count: int, goal: int) -> int`
  - Count consecutive days (ending today or yesterday) where count >= goal
  - Must handle gaps in dates (non-consecutive dates break streak)
- [x] Add tests for streak logic:
  - No streak when today below goal
  - Streak continues from yesterday
  - Gaps break streak
  - Streak includes today if today >= goal

**Implementation Details:**
- Added `calculate_streak(history: dict, today: str, today_count: int, goal: int) -> int` function in `tui_clock/main.py:120-167`
- If today meets goal, starts streak at 1 and walks backwards from yesterday
- If today doesn't meet goal, walks backwards starting from yesterday
- Handles gaps by checking if date string exists in history dict
- Days below goal break the streak
- Uses `datetime.strptime` and `timedelta` for date arithmetic
- Added 11 tests in `tests/test_water.py` class `TestCalculateStreak`:
  - `test_no_streak_when_today_below_goal_and_no_history` - empty history, today below goal = 0
  - `test_streak_of_one_when_only_today_meets_goal` - only today meets goal = 1
  - `test_streak_continues_from_yesterday` - both days meet goal = 2
  - `test_streak_from_multiple_consecutive_days` - 4 consecutive days = 4
  - `test_gap_in_dates_breaks_streak` - missing date breaks streak
  - `test_day_below_goal_breaks_streak` - day below goal breaks streak
  - `test_streak_from_yesterday_when_today_below_goal` - streak from yesterday when today doesn't count
  - `test_no_streak_when_yesterday_below_goal_and_today_below_goal` - no streak at all
  - `test_today_exactly_at_goal_counts` - goal boundary test
  - `test_empty_history_today_meets_goal` - edge case with no history
  - `test_long_streak_broken_early` - long streak broken by one bad day

### P5: Water Stats Popup ✅ COMPLETED
- [x] Create `WaterStatsPopup` widget (modal overlay)
- [x] Display on keybinding (`w` key)
- [x] Layout:
  ```
  💧 {count}/{goal}     (or just 💧 {count} if goal disabled)
  🔥 {streak} days      (if show_streak enabled)
  🏆 {record}           (if show_record enabled)
  ```
- [x] Style popup consistently with existing app theme
- [x] Dismiss popup on click or key press (Escape, Q)
- [x] Add tests for popup visibility and content

**Implementation Details:**
- Created `WaterStatsPopup(ModalScreen)` class in `tui_clock/main.py:34-96`
- Popup extends Textual's `ModalScreen` for proper modal behavior
- Accepts count, goal, streak, and record as constructor parameters
- Only displays streak/record lines when those values are not None
- Uses inline CSS via `DEFAULT_CSS` for consistent styling with app theme
- Added `action_show_water_stats()` method in `TuiClockApp` to compute and display stats
- Added `w` keybinding to trigger `action_show_water_stats`
- Streak is computed only when `show_streak=True` AND `daily_goal` is set
- Record is computed only when `show_record=True`
- Added 10 tests in `tests/test_water.py`:
  - `TestWaterStatsPopup` class (6 tests): popup initialization and format strings
  - `TestWaterStatsIntegration` class (4 tests): config integration with app

### P6: Integration & Polish
- [x] Wire config to app startup (already done in P1)
- [ ] Update `_check_water` and `on_click` to refresh streak/record displays (not needed - popup shows live calculations)
- [ ] Ensure streak/record update when day changes at midnight (handled by existing `_check_water` day change detection)
- [ ] Add example config file to README or create `.tui_clock.toml.example`

## Notes

- **Existing infrastructure**: History is already persisted in `.water_stats["history"]` as `{date: count}` pairs. The daily record and streak can be computed from this without new storage.
- **No breaking changes**: Features are opt-in with default `false`, preserving existing behavior.
- **Testing**: Each feature should have unit tests. Consider using freezegun or manual mocking for date-dependent logic.
- **No external TOML dependency**: Python 3.11+ includes `tomllib` in stdlib, so no new dependency needed.

## Files Modified

- `tui_clock/config.py` - NEW: Config loading module
- `tui_clock/main.py` - Added config import and loading in `TuiClockApp.__init__`; P2: added `_get_display_goal()` helper and updated `WaterCounter.update_count()` with optional goal parameter; P3: added `calculate_daily_record()` function; P4: added `calculate_streak()` function; P5: added `WaterStatsPopup` modal screen class and `action_show_water_stats()` method with `w` keybinding
- `tests/test_config.py` - NEW: Config tests (15 tests)
- `tests/test_water.py` - NEW: Water counter and goal display tests (8 tests); P3: added 7 tests for daily record calculation; P4: added 11 tests for streak calculation; P5: added 10 tests for popup (6 in `TestWaterStatsPopup`, 4 in `TestWaterStatsIntegration`)
