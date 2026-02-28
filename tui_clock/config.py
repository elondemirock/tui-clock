"""Configuration loading for tui-clock."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class Config:
    """Application configuration."""

    daily_goal: int | None = None
    show_goal: bool = False
    show_streak: bool = False
    show_record: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create config from a dictionary, using defaults for missing values."""
        return cls(
            daily_goal=data.get("daily_goal"),
            show_goal=data.get("show_goal", False),
            show_streak=data.get("show_streak", False),
            show_record=data.get("show_record", False),
        )


def get_config_paths() -> list[Path]:
    """Return possible config file paths in priority order."""
    paths = []

    # Project-local config (highest priority)
    paths.append(Path.cwd() / ".tui_clock.toml")

    # XDG config directory
    xdg_config = Path.home() / ".config" / "tui-clock" / "config.toml"
    paths.append(xdg_config)

    return paths


def load_config() -> Config:
    """Load configuration from the first available config file.

    Searches for config files in this order:
    1. .tui_clock.toml in current directory
    2. ~/.config/tui-clock/config.toml

    Returns default Config if no config file is found.
    """
    for path in get_config_paths():
        if path.exists():
            try:
                with open(path, "rb") as f:
                    data = tomllib.load(f)
                return Config.from_dict(data)
            except (tomllib.TOMLDecodeError, OSError):
                # Invalid TOML or read error - continue to next path
                continue

    return Config()
