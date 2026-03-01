"""Tests for water tracking features."""

from tui_clock.config import Config
from tui_clock.main import TuiClockApp, calculate_daily_record, calculate_streak


def test_get_display_goal():
    assert TuiClockApp(config=Config(daily_goal=8, show_goal=True))._get_display_goal() == 8
    assert TuiClockApp(config=Config(daily_goal=8, show_goal=False))._get_display_goal() is None
    assert TuiClockApp(config=Config())._get_display_goal() is None


def test_calculate_daily_record():
    assert calculate_daily_record({}, 5) == 5
    assert calculate_daily_record({"2026-02-27": 10}, 5) == 10
    assert calculate_daily_record({"2026-02-27": 3}, 8) == 8


def test_calculate_streak_consecutive():
    assert calculate_streak({}, "2026-02-28", 8, 8) == 1
    assert calculate_streak({"2026-02-27": 10}, "2026-02-28", 8, 8) == 2
    history = {"2026-02-25": 9, "2026-02-26": 10, "2026-02-27": 8}
    assert calculate_streak(history, "2026-02-28", 12, 8) == 4


def test_calculate_streak_breaks():
    # Gap in dates breaks streak
    assert calculate_streak({"2026-02-25": 10, "2026-02-27": 10}, "2026-02-28", 10, 8) == 2
    # Day below goal breaks streak
    assert calculate_streak({"2026-02-25": 10, "2026-02-26": 5, "2026-02-27": 10}, "2026-02-28", 10, 8) == 2


def test_calculate_streak_today_below_goal():
    assert calculate_streak({}, "2026-02-28", 3, 8) == 0
    assert calculate_streak({"2026-02-26": 10, "2026-02-27": 9}, "2026-02-28", 5, 8) == 2
