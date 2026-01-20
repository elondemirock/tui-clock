"""Main TUI clock application."""

from datetime import datetime

import pytz
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static

from tui_clock.digits import render_time_large

PT_TIMEZONE = pytz.timezone("America/Los_Angeles")
ET_TIMEZONE = pytz.timezone("America/New_York")

# Blink configuration
BLINK_MINUTES = (0, 30)  # Blink at :00 and :30
BLINK_DURATION = 0.15  # Duration of each blink phase in seconds
BLINK_COUNT = 3  # Number of blink cycles


class ClockDisplay(Static):
    """Widget displaying the large ASCII art clock."""

    def on_mount(self) -> None:
        """Start the clock update timer when mounted."""
        self.update_clock()
        self.set_interval(1.0, self.update_clock)

    def update_clock(self) -> None:
        """Update the clock display with current PT time."""
        now = datetime.now(PT_TIMEZONE)
        time_str = now.strftime("%H:%M")
        ascii_time = render_time_large(time_str)
        self.update(ascii_time)


class SecondaryDisplay(Static):
    """Widget displaying the ET time in smaller text."""

    def on_mount(self) -> None:
        """Start the ET time update timer when mounted."""
        self.update_time()
        self.set_interval(1.0, self.update_time)

    def update_time(self) -> None:
        """Update the secondary display with ET time."""
        now = datetime.now(ET_TIMEZONE)
        time_str = now.strftime("%H:%M")
        self.update(f"ET: {time_str}")


def should_blink(minute: int) -> bool:
    """Check if the current minute should trigger a blink."""
    return minute in BLINK_MINUTES


class TuiClockApp(App):
    """A TUI clock application displaying PT and ET time."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }

    Screen.blink {
        background: white;
    }

    Screen.blink ClockDisplay {
        color: black;
    }

    Screen.blink SecondaryDisplay {
        color: black;
    }

    #clock-container {
        width: auto;
        height: auto;
        align: center middle;
    }

    ClockDisplay {
        text-align: center;
        color: $text;
        text-style: bold;
        width: auto;
        height: auto;
    }

    SecondaryDisplay {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
        width: auto;
        height: auto;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        """Initialize the app with blink tracking state."""
        super().__init__()
        self._last_blink_minute: int | None = None
        self._blink_count = 0

    def on_mount(self) -> None:
        """Start the blink check timer when app mounts."""
        self.set_interval(1.0, self._check_blink)

    def _check_blink(self) -> None:
        """Check if we should trigger a blink at the current time."""
        now = datetime.now(PT_TIMEZONE)
        current_minute = now.minute

        if should_blink(current_minute) and self._last_blink_minute != current_minute:
            self._last_blink_minute = current_minute
            self._start_blink()

    def _start_blink(self) -> None:
        """Start the blink animation sequence."""
        self._blink_count = 0
        self._do_blink_on()

    def _do_blink_on(self) -> None:
        """Turn blink on (inverted colors)."""
        self.screen.add_class("blink")
        self.set_timer(BLINK_DURATION, self._do_blink_off)

    def _do_blink_off(self) -> None:
        """Turn blink off (normal colors)."""
        self.screen.remove_class("blink")
        self._blink_count += 1
        if self._blink_count < BLINK_COUNT:
            self.set_timer(BLINK_DURATION, self._do_blink_on)

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        with Container(id="clock-container"):
            with Vertical():
                yield ClockDisplay()
                yield SecondaryDisplay()


def main() -> None:
    """Run the TUI clock application."""
    app = TuiClockApp()
    app.run()


if __name__ == "__main__":
    main()
