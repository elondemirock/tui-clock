"""Main TUI clock application."""

from datetime import datetime

import pytz
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static

from tui_clock.digits import render_time_large

PT_TIMEZONE = pytz.timezone("America/Los_Angeles")
ET_TIMEZONE = pytz.timezone("America/New_York")


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


class TuiClockApp(App):
    """A TUI clock application displaying PT and ET time."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
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
