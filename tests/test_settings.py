"""Tests for game config and settings loading."""

from __future__ import annotations

import os

import pytest

from orchestrator.models import GameConfig
from orchestrator.settings import load_dotenv, load_game_config, load_settings


def test_gta6_config_loads() -> None:
    game = load_game_config("gta6")
    assert isinstance(game, GameConfig)
    assert game.slug == "gta6"
    assert game.name == "Grand Theft Auto VI"
    assert "PS5" in game.platforms
    assert game.ip_safety.get("forbid_leaks") is True
    assert len(game.ip_safety.get("banned_patterns", [])) > 0


def test_settings_loads_with_game() -> None:
    settings = load_settings(game_slug="gta6", dry_run=True, use_dotenv=False)
    assert settings.game.slug == "gta6"
    assert settings.dry_run is True
    variables = settings.as_variables()
    assert variables["game"] == "Grand Theft Auto VI"
    assert "platforms" in variables


def test_load_game_config_missing_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_game_config("nonexistent-game-slug")


def test_load_dotenv_parses_and_sets_env(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text('RELEASE_DATE="2026-11-19"\n# comment\nFOO=bar\n', encoding="utf-8")
    monkeypatch.delenv("FOO", raising=False)
    parsed = load_dotenv(env_file)
    assert parsed["FOO"] == "bar"
    assert os.environ.get("FOO") == "bar"


def test_example_game_config_loads() -> None:
    game = load_game_config("example")
    assert game.slug == "example"
    assert game.name == "Example Game"


def test_settings_release_date_env_override(monkeypatch) -> None:
    monkeypatch.setenv("RELEASE_DATE", "2026-12-01")
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    assert settings.game.release_date == "2026-12-01"
