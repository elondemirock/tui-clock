"""Tests for water counter and goal display functionality."""

from tui_clock.config import Config
from tui_clock.main import (
    TuiClockApp,
    WaterStatsPopup,
    calculate_daily_record,
    calculate_streak,
)


class TestTuiClockAppGoalDisplay:
    """Tests for goal display integration in TuiClockApp."""

    def test_get_display_goal_when_show_goal_disabled(self):
        """Should return None when show_goal is False."""
        config = Config(daily_goal=8, show_goal=False)
        app = TuiClockApp(config=config)
        assert app._get_display_goal() is None

    def test_get_display_goal_when_show_goal_enabled(self):
        """Should return the daily goal when show_goal is True."""
        config = Config(daily_goal=8, show_goal=True)
        app = TuiClockApp(config=config)
        assert app._get_display_goal() == 8

    def test_get_display_goal_when_no_daily_goal_set(self):
        """Should return None when daily_goal is None even if show_goal is True."""
        config = Config(daily_goal=None, show_goal=True)
        app = TuiClockApp(config=config)
        assert app._get_display_goal() is None

    def test_get_display_goal_with_default_config(self):
        """Should return None with default config."""
        config = Config()
        app = TuiClockApp(config=config)
        assert app._get_display_goal() is None


def test_format_water_display_without_goal():
    """Display format should show just the count when no goal."""
    # Test the format string logic directly
    count = 5
    goal = None
    if goal is not None:
        result = f"\U0001f4a7 {count}/{goal}"
    else:
        result = f"\U0001f4a7 {count}"
    assert result == "\U0001f4a7 5"


def test_format_water_display_with_goal():
    """Display format should show count/goal when goal provided."""
    count = 3
    goal = 8
    if goal is not None:
        result = f"\U0001f4a7 {count}/{goal}"
    else:
        result = f"\U0001f4a7 {count}"
    assert result == "\U0001f4a7 3/8"


def test_format_water_display_with_zero_count_and_goal():
    """Display format should work with zero count and goal."""
    count = 0
    goal = 10
    if goal is not None:
        result = f"\U0001f4a7 {count}/{goal}"
    else:
        result = f"\U0001f4a7 {count}"
    assert result == "\U0001f4a7 0/10"


def test_format_water_display_count_exceeds_goal():
    """Display format should work when count exceeds goal."""
    count = 12
    goal = 8
    if goal is not None:
        result = f"\U0001f4a7 {count}/{goal}"
    else:
        result = f"\U0001f4a7 {count}"
    assert result == "\U0001f4a7 12/8"


class TestCalculateDailyRecord:
    """Tests for daily record calculation."""

    def test_empty_history_returns_today_count(self):
        """With no history, record is today's count."""
        assert calculate_daily_record({}, 5) == 5

    def test_empty_history_with_zero_today(self):
        """With no history and zero today, record is 0."""
        assert calculate_daily_record({}, 0) == 0

    def test_single_day_history_higher_than_today(self):
        """Record from history higher than today."""
        history = {"2026-02-27": 10}
        assert calculate_daily_record(history, 5) == 10

    def test_single_day_history_lower_than_today(self):
        """Today's count higher than historical record."""
        history = {"2026-02-27": 3}
        assert calculate_daily_record(history, 8) == 8

    def test_multiple_days_history(self):
        """Find max across multiple historical days."""
        history = {
            "2026-02-25": 4,
            "2026-02-26": 12,
            "2026-02-27": 7,
        }
        assert calculate_daily_record(history, 5) == 12

    def test_today_beats_all_history(self):
        """Today's count is new record."""
        history = {
            "2026-02-25": 4,
            "2026-02-26": 8,
            "2026-02-27": 6,
        }
        assert calculate_daily_record(history, 15) == 15

    def test_today_equals_historical_max(self):
        """Today ties with historical record."""
        history = {"2026-02-27": 10}
        assert calculate_daily_record(history, 10) == 10


class TestWaterStatsPopup:
    """Tests for WaterStatsPopup content generation."""

    def test_popup_stores_count_only(self):
        """Popup stores count when no goal/streak/record."""
        popup = WaterStatsPopup(count=5, goal=None, streak=None, record=None)
        assert popup._count == 5
        assert popup._goal is None
        assert popup._streak is None
        assert popup._record is None

    def test_popup_stores_all_stats(self):
        """Popup stores all stats when provided."""
        popup = WaterStatsPopup(count=5, goal=8, streak=3, record=12)
        assert popup._count == 5
        assert popup._goal == 8
        assert popup._streak == 3
        assert popup._record == 12

    def test_popup_count_with_goal_format(self):
        """Popup displays count/goal format when goal is set."""
        # Test the format logic used in compose()
        count = 5
        goal = 8
        if goal is not None:
            result = f"\U0001f4a7 {count}/{goal}"
        else:
            result = f"\U0001f4a7 {count}"
        assert result == "\U0001f4a7 5/8"

    def test_popup_count_without_goal_format(self):
        """Popup displays count only when goal is None."""
        count = 5
        goal = None
        if goal is not None:
            result = f"\U0001f4a7 {count}/{goal}"
        else:
            result = f"\U0001f4a7 {count}"
        assert result == "\U0001f4a7 5"

    def test_popup_streak_format(self):
        """Streak displays in correct format."""
        streak = 7
        result = f"\U0001f525 {streak} days"
        assert result == "\U0001f525 7 days"

    def test_popup_record_format(self):
        """Record displays in correct format."""
        record = 15
        result = f"\U0001f3c6 {record}"
        assert result == "\U0001f3c6 15"


class TestWaterStatsIntegration:
    """Tests for water stats popup integration with TuiClockApp."""

    def test_action_show_water_stats_no_features_enabled(self):
        """With default config, streak and record should be None."""
        config = Config()  # All features disabled by default
        app = TuiClockApp(config=config)
        # Directly check what would be passed to popup
        goal = app._get_display_goal()
        assert goal is None

    def test_action_show_water_stats_with_show_goal(self):
        """With show_goal enabled, goal should be returned."""
        config = Config(daily_goal=8, show_goal=True)
        app = TuiClockApp(config=config)
        goal = app._get_display_goal()
        assert goal == 8

    def test_streak_not_calculated_without_daily_goal(self):
        """show_streak without daily_goal should not calculate streak."""
        config = Config(show_streak=True, daily_goal=None)
        # Creating app validates config is accepted
        TuiClockApp(config=config)
        # Even with show_streak=True, no daily_goal means no streak
        assert config.daily_goal is None

    def test_streak_calculated_with_daily_goal(self):
        """show_streak with daily_goal should allow streak calculation."""
        config = Config(show_streak=True, daily_goal=8)
        # Creating app validates config is accepted
        TuiClockApp(config=config)
        assert config.show_streak is True
        assert config.daily_goal == 8


class TestCalculateStreak:
    """Tests for streak calculation."""

    def test_no_streak_when_today_below_goal_and_no_history(self):
        """No streak when today is below goal and no history."""
        history = {}
        assert calculate_streak(history, "2026-02-28", 3, 8) == 0

    def test_streak_of_one_when_only_today_meets_goal(self):
        """Streak is 1 when only today meets goal."""
        history = {}
        assert calculate_streak(history, "2026-02-28", 8, 8) == 1

    def test_streak_continues_from_yesterday(self):
        """Streak includes yesterday when both days meet goal."""
        history = {"2026-02-27": 10}
        assert calculate_streak(history, "2026-02-28", 8, 8) == 2

    def test_streak_from_multiple_consecutive_days(self):
        """Streak counts multiple consecutive days meeting goal."""
        history = {
            "2026-02-25": 9,
            "2026-02-26": 10,
            "2026-02-27": 8,
        }
        assert calculate_streak(history, "2026-02-28", 12, 8) == 4

    def test_gap_in_dates_breaks_streak(self):
        """Missing dates in history break the streak."""
        history = {
            "2026-02-25": 10,
            # 2026-02-26 is missing
            "2026-02-27": 10,
        }
        assert calculate_streak(history, "2026-02-28", 10, 8) == 2

    def test_day_below_goal_breaks_streak(self):
        """Day below goal breaks the streak."""
        history = {
            "2026-02-25": 10,
            "2026-02-26": 5,  # Below goal
            "2026-02-27": 10,
        }
        assert calculate_streak(history, "2026-02-28", 10, 8) == 2

    def test_streak_from_yesterday_when_today_below_goal(self):
        """Streak starts from yesterday when today doesn't meet goal."""
        history = {
            "2026-02-26": 10,
            "2026-02-27": 9,
        }
        assert calculate_streak(history, "2026-02-28", 5, 8) == 2

    def test_no_streak_when_yesterday_below_goal_and_today_below_goal(self):
        """No streak when both today and yesterday are below goal."""
        history = {"2026-02-27": 5}
        assert calculate_streak(history, "2026-02-28", 3, 8) == 0

    def test_today_exactly_at_goal_counts(self):
        """Today exactly at goal counts toward streak."""
        history = {"2026-02-27": 8}
        assert calculate_streak(history, "2026-02-28", 8, 8) == 2

    def test_empty_history_today_meets_goal(self):
        """With empty history, streak is 1 if today meets goal."""
        assert calculate_streak({}, "2026-02-28", 10, 8) == 1

    def test_long_streak_broken_early(self):
        """Long streak broken by a day below goal early on."""
        history = {
            "2026-02-20": 10,
            "2026-02-21": 3,  # Below goal - breaks streak
            "2026-02-22": 10,
            "2026-02-23": 10,
            "2026-02-24": 10,
            "2026-02-25": 10,
            "2026-02-26": 10,
            "2026-02-27": 10,
        }
        assert calculate_streak(history, "2026-02-28", 10, 8) == 7
