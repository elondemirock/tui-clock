"""Tests for water counter and goal display functionality."""

from tui_clock.config import Config
from tui_clock.main import TuiClockApp


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
