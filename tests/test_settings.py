"""Tests for game config and settings loading."""

from __future__ import annotations

from orchestrator.models import GameConfig
from orchestrator.settings import load_game_config, load_settings


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
