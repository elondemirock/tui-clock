"""Tests for configuration loading."""

from pathlib import Path

import pytest

from tui_clock.config import Config, get_config_paths, load_config


def test_config_defaults():
    """Default config should have all features disabled."""
    config = Config()
    assert config.daily_goal is None
    assert config.show_goal is False
    assert config.show_streak is False
    assert config.show_record is False


def test_config_from_dict_with_all_values():
    """Config should load all values from dict."""
    data = {
        "daily_goal": 8,
        "show_goal": True,
        "show_streak": True,
        "show_record": True,
    }
    config = Config.from_dict(data)
    assert config.daily_goal == 8
    assert config.show_goal is True
    assert config.show_streak is True
    assert config.show_record is True


def test_config_from_dict_with_partial_values():
    """Config should use defaults for missing values."""
    data = {"daily_goal": 6, "show_goal": True}
    config = Config.from_dict(data)
    assert config.daily_goal == 6
    assert config.show_goal is True
    assert config.show_streak is False
    assert config.show_record is False


def test_config_from_empty_dict():
    """Config from empty dict should use all defaults."""
    config = Config.from_dict({})
    assert config.daily_goal is None
    assert config.show_goal is False
    assert config.show_streak is False
    assert config.show_record is False


def test_get_config_paths_returns_expected_locations():
    """Config paths should include local and XDG locations."""
    paths = get_config_paths()
    assert len(paths) == 2
    # First path should be local
    assert paths[0].name == ".tui_clock.toml"
    # Second path should be in .config
    assert "config" in str(paths[1])
    assert paths[1].name == "config.toml"


def test_load_config_returns_defaults_when_no_file(monkeypatch, tmp_path):
    """load_config should return defaults when no config file exists."""
    monkeypatch.chdir(tmp_path)
    # Patch home to avoid reading user's actual config
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")

    config = load_config()
    assert config == Config()


def test_load_config_reads_local_file(monkeypatch, tmp_path):
    """load_config should read .tui_clock.toml from current directory."""
    config_file = tmp_path / ".tui_clock.toml"
    config_file.write_text(
        """\
daily_goal = 10
show_goal = true
show_streak = true
"""
    )
    monkeypatch.chdir(tmp_path)
    # Patch home to avoid reading user's actual config
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")

    config = load_config()
    assert config.daily_goal == 10
    assert config.show_goal is True
    assert config.show_streak is True
    assert config.show_record is False


def test_load_config_reads_xdg_file(monkeypatch, tmp_path):
    """load_config should read from ~/.config/tui-clock/config.toml."""
    # Create XDG config
    xdg_dir = tmp_path / ".config" / "tui-clock"
    xdg_dir.mkdir(parents=True)
    config_file = xdg_dir / "config.toml"
    config_file.write_text(
        """\
daily_goal = 7
show_record = true
"""
    )
    # Create and chdir to a different directory (no local config)
    other_dir = tmp_path / "some_other_dir"
    other_dir.mkdir(exist_ok=True)
    monkeypatch.chdir(other_dir)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()
    assert config.daily_goal == 7
    assert config.show_record is True
    assert config.show_goal is False


def test_load_config_local_takes_priority(monkeypatch, tmp_path):
    """Local config should take priority over XDG config."""
    # Create XDG config
    xdg_dir = tmp_path / ".config" / "tui-clock"
    xdg_dir.mkdir(parents=True)
    xdg_config = xdg_dir / "config.toml"
    xdg_config.write_text("daily_goal = 5\n")

    # Create local config
    local_config = tmp_path / ".tui_clock.toml"
    local_config.write_text("daily_goal = 12\n")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()
    assert config.daily_goal == 12


def test_load_config_handles_invalid_toml(monkeypatch, tmp_path):
    """load_config should handle invalid TOML gracefully."""
    config_file = tmp_path / ".tui_clock.toml"
    config_file.write_text("this is not valid toml [[[")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")

    # Should return defaults instead of crashing
    config = load_config()
    assert config == Config()


def test_config_is_immutable():
    """Config dataclass should be frozen (immutable)."""
    config = Config(daily_goal=5)
    with pytest.raises(AttributeError):
        config.daily_goal = 10  # type: ignore
