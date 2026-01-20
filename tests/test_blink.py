"""Tests for the 30-minute screen blink feature."""

from tui_clock.main import BLINK_MINUTES, should_blink


def test_should_blink_at_zero_minutes():
    """Should blink when minute is 0."""
    assert should_blink(0) is True


def test_should_blink_at_thirty_minutes():
    """Should blink when minute is 30."""
    assert should_blink(30) is True


def test_should_not_blink_at_other_minutes():
    """Should not blink at minutes other than 0 and 30."""
    non_blink_minutes = [1, 15, 29, 31, 45, 59]
    for minute in non_blink_minutes:
        assert should_blink(minute) is False, f"Should not blink at minute {minute}"


def test_blink_minutes_config():
    """Verify blink minutes configuration."""
    assert BLINK_MINUTES == (0, 30)
