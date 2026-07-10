"""Load game config and environment-backed runtime settings."""

from __future__ import annotations

import os
from pathlib import Path

from orchestrator.models import GameConfig, Settings
from orchestrator.utils import PROJECT_ROOT, load_yaml


def _config_dir() -> Path:
    return PROJECT_ROOT / "config" / "games"


def load_game_config(slug: str) -> GameConfig:
    """Load a game config YAML by slug (e.g. gta6)."""
    path = _config_dir() / f"{slug}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No game config found: {path}")

    raw = load_yaml(path)
    return GameConfig(
        slug=str(raw.get("slug", slug)),
        name=str(raw["name"]),
        release_date=str(raw.get("release_date", "")),
        platforms=list(raw.get("platforms", [])),
        official_sources=list(raw.get("official_sources", [])),
        coverage_sources=list(raw.get("coverage_sources", [])),
        ip_safety=dict(raw.get("ip_safety", {})),
        content_tags=list(raw.get("content_tags", [])),
        community_channels=dict(raw.get("community_channels", {})),
        monetization_categories=list(raw.get("monetization_categories", [])),
    )


def load_dotenv(path: str | os.PathLike[str] | None = None, *, override: bool = False) -> dict[str, str]:
    """Load simple KEY=VALUE pairs from a `.env` file into os.environ."""
    env_path = Path(path) if path is not None else PROJECT_ROOT / ".env"
    parsed: dict[str, str] = {}
    if not env_path.exists():
        return parsed

    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        parsed[key] = value
        if override or key not in os.environ:
            os.environ[key] = value
    return parsed


def load_settings(
    *,
    game_slug: str | None = None,
    dry_run: bool = True,
    use_dotenv: bool = True,
    extra: dict[str, str] | None = None,
) -> Settings:
    """Build Settings from game config and environment."""
    if use_dotenv:
        load_dotenv()

    slug = game_slug or os.environ.get("GAME_SLUG", "gta6")
    game = load_game_config(slug)

    if os.environ.get("RELEASE_DATE"):
        game.release_date = os.environ["RELEASE_DATE"]

    return Settings(game=game, dry_run=dry_run, extra=extra or {})
