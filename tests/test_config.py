"""Tests for configuration loading."""

from pathlib import Path
from tui_clock.config import Config, load_config


def test_config_defaults():
    config = Config()
    assert config.daily_goal is None
    assert config.show_goal is False
    assert config.show_streak is False


def test_config_from_dict():
    config = Config.from_dict({"daily_goal": 8, "show_goal": True})
    assert config.daily_goal == 8
    assert config.show_goal is True
    assert config.show_streak is False


def test_load_config_returns_defaults_when_no_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")
    assert load_config() == Config()


def test_load_config_reads_local_file(monkeypatch, tmp_path):
    (tmp_path / ".tui_clock.toml").write_text("daily_goal = 10\nshow_goal = true\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")
    config = load_config()
    assert config.daily_goal == 10
    assert config.show_goal is True


def test_load_config_handles_invalid_toml(monkeypatch, tmp_path):
    (tmp_path / ".tui_clock.toml").write_text("invalid [[[")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "fake_home")
    assert load_config() == Config()
