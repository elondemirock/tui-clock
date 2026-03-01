"""Configuration loading for tui-clock."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    """Application configuration."""
    daily_goal: int | None = None
    show_goal: bool = False
    show_streak: bool = False
    show_record: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        return cls(
            daily_goal=data.get("daily_goal"),
            show_goal=data.get("show_goal", False),
            show_streak=data.get("show_streak", False),
            show_record=data.get("show_record", False),
        )


def load_config() -> Config:
    """Load config from .tui_clock.toml (local) or ~/.config/tui-clock/config.toml."""
    paths = [Path.cwd() / ".tui_clock.toml", Path.home() / ".config/tui-clock/config.toml"]
    for path in paths:
        if path.exists():
            try:
                with open(path, "rb") as f:
                    return Config.from_dict(tomllib.load(f))
            except (tomllib.TOMLDecodeError, OSError):
                continue
    return Config()
