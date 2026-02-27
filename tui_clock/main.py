"""Main TUI clock application."""

import json
from datetime import datetime
from pathlib import Path

import pytz
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.widgets import Static

from tui_clock.digits import render_time_large

WATER_STATS_FILE = Path(__file__).resolve().parent.parent / ".water_stats"

PT_TIMEZONE = pytz.timezone("America/Los_Angeles")
ET_TIMEZONE = pytz.timezone("America/New_York")

# Blink configuration
BLINK_MINUTES = (0, 30)  # Blink at :00 and :30
BLINK_DURATION = 0.15  # Duration of each blink phase in seconds
BLINK_COUNT = 3  # Number of blink cycles

# Water reminder configuration
WATER_INTERVAL = 15  # Remind every 15 minutes
WATER_START_HOUR = 8  # 8 AM PT
WATER_END_HOUR = 18  # 6 PM PT
WATER_BLINK_DURATION = 0.15
WATER_BLINK_COUNT = 5


class WaterCounter(Static):
    """Widget displaying the water counter at the top left."""

    def update_count(self, count: int) -> None:
        self.update(f"\U0001f4a7 {count}")


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


class ETDisplay(Static):
    """Widget displaying the ET time."""

    def on_mount(self) -> None:
        """Start the ET time update timer when mounted."""
        self.update_time()
        self.set_interval(1.0, self.update_time)

    def update_time(self) -> None:
        """Update with ET time."""
        now = datetime.now(ET_TIMEZONE)
        time_str = now.strftime("%H:%M")
        self.update(f"ET: {time_str}")


def _load_water_stats() -> dict:
    """Load water stats from disk. Resets today_count if it's a new day."""
    today = datetime.now(ET_TIMEZONE).strftime("%Y-%m-%d")
    default = {"today": today, "today_count": 0, "history": {}}
    try:
        data = json.loads(WATER_STATS_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default
    if data.get("today") != today:
        # New day — archive yesterday and reset
        if data.get("today") and data.get("today_count", 0) > 0:
            data.setdefault("history", {})[data["today"]] = data["today_count"]
        data["today"] = today
        data["today_count"] = 0
        _save_water_stats(data)
    return data


def _save_water_stats(data: dict) -> None:
    """Save water stats to disk."""
    WATER_STATS_FILE.write_text(json.dumps(data, indent=2) + "\n")


def should_blink(minute: int) -> bool:
    """Check if the current minute should trigger a blink."""
    return minute in BLINK_MINUTES


def should_drink_water(now_pt: datetime) -> bool:
    """Check if it's time for a water reminder."""
    return (
        WATER_START_HOUR <= now_pt.hour < WATER_END_HOUR
        and now_pt.minute % WATER_INTERVAL == 0
    )


class TuiClockApp(App):
    """A TUI clock application displaying PT and ET time."""

    CSS = """
    Screen {
        background: $surface;
    }

    Screen.blink {
        background: white;
    }

    Screen.blink ClockDisplay {
        color: black;
    }

    Screen.blink #top-row {
        color: black;
    }

    Screen.water-alert {
        background: cyan;
    }

    Screen.water-alert ClockDisplay {
        color: black;
    }

    Screen.water-alert #top-row {
        color: black;
    }

    Screen.water-alert WaterCounter {
        color: black;
        text-style: bold;
    }

    #top-row {
        width: 100%;
        height: 1;
        color: $text-muted;
    }

    WaterCounter {
        width: 1fr;
        height: 1;
        padding-left: 1;
    }

    ETDisplay {
        width: auto;
        height: 1;
        padding-right: 1;
    }

    ClockDisplay {
        text-align: center;
        color: $text;
        text-style: bold;
        width: 100%;
        height: auto;
    }

    #spacer {
        height: 1;
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
        self._last_water_minute: int | None = None
        self._water_blink_count = 0
        self._water_stats = _load_water_stats()
        self._water_count = self._water_stats["today_count"]
        self._waiting_for_click = False

    def on_mount(self) -> None:
        """Start the blink check timer when app mounts."""
        self.set_interval(1.0, self._check_blink)
        self.set_interval(1.0, self._check_water)
        self.query_one(WaterCounter).update_count(self._water_count)

    def on_click(self, event: Click) -> None:
        """Handle click to acknowledge water reminder."""
        if self._waiting_for_click:
            self._waiting_for_click = False
            self._water_count += 1
            self._water_stats["today_count"] = self._water_count
            _save_water_stats(self._water_stats)
            self.screen.remove_class("water-alert")
            self.query_one(WaterCounter).update_count(self._water_count)

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
        if self._waiting_for_click:
            self.screen.remove_class("water-alert")
        self.screen.add_class("blink")
        self.set_timer(BLINK_DURATION, self._do_blink_off)

    def _do_blink_off(self) -> None:
        """Turn blink off (normal colors)."""
        self.screen.remove_class("blink")
        self._blink_count += 1
        if self._blink_count < BLINK_COUNT:
            self.set_timer(BLINK_DURATION, self._do_blink_on)
        elif self._waiting_for_click:
            self.screen.add_class("water-alert")

    def _check_water(self) -> None:
        """Check if we should trigger a water reminder."""
        # Reset counter if the day has changed while the app is running
        today = datetime.now(ET_TIMEZONE).strftime("%Y-%m-%d")
        if self._water_stats.get("today") != today:
            self._water_stats = _load_water_stats()
            self._water_count = self._water_stats["today_count"]
            self.query_one(WaterCounter).update_count(self._water_count)

        if self._waiting_for_click:
            return
        now_pt = datetime.now(PT_TIMEZONE)
        current_minute = now_pt.hour * 60 + now_pt.minute

        if should_drink_water(now_pt) and self._last_water_minute != current_minute:
            self._last_water_minute = current_minute
            self._start_water_blink()

    def _start_water_blink(self) -> None:
        """Start the water reminder blink, then stay lit until click."""
        self._water_blink_count = 0
        self._do_water_blink_on()

    def _do_water_blink_on(self) -> None:
        """Turn water blink on."""
        self.screen.add_class("water-alert")
        self.set_timer(WATER_BLINK_DURATION, self._do_water_blink_off)

    def _do_water_blink_off(self) -> None:
        """Turn water blink off."""
        self.screen.remove_class("water-alert")
        self._water_blink_count += 1
        if self._water_blink_count < WATER_BLINK_COUNT:
            self.set_timer(WATER_BLINK_DURATION, self._do_water_blink_on)
        else:
            # Done blinking — stay lit and wait for click
            self.screen.add_class("water-alert")
            self._waiting_for_click = True

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        with Horizontal(id="top-row"):
            yield WaterCounter()
            yield ETDisplay()
        yield ClockDisplay()
        yield Static("", id="spacer")


def main() -> None:
    """Run the TUI clock application."""
    app = TuiClockApp()
    app.run()


if __name__ == "__main__":
    main()
