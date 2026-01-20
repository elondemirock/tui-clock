"""Tests for ASCII digit rendering."""

from tui_clock.digits import LARGE_DIGITS, render_time_large


def test_all_digits_have_same_height():
    """All digit representations should have the same number of lines."""
    expected_height = 7
    for digit, lines in LARGE_DIGITS.items():
        assert len(lines) == expected_height, f"Digit '{digit}' has {len(lines)} lines"


def test_all_digits_have_same_width():
    """All lines in each digit should have the same width."""
    expected_width = 6
    for digit, lines in LARGE_DIGITS.items():
        for i, line in enumerate(lines):
            assert len(line) == expected_width, (
                f"Digit '{digit}' line {i} has width {len(line)}"
            )


def test_render_time_produces_correct_lines():
    """Rendering a time should produce 7 lines of ASCII art."""
    result = render_time_large("12:34")
    lines = result.split("\n")
    assert len(lines) == 7


def test_render_time_contains_all_digits():
    """Rendered time should include all specified digits."""
    result = render_time_large("00:00")
    # Should have ASCII art for zeros
    assert "█" in result


def test_colon_is_rendered():
    """The colon character should be rendered in time display."""
    result = render_time_large("12:34")
    # Colon pattern has empty spaces in specific rows
    lines = result.split("\n")
    # Colon has blocks on lines 1, 2, 4, 5 (0-indexed)
    assert "██" in lines[1]  # Should have colon blocks
