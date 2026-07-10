"""Shared helpers for YAML loading and timestamps."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return the parsed mapping."""
    file_path = Path(path)
    with file_path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {file_path}, got {type(data).__name__}")
    return data


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def epoch_ms() -> int:
    """Return current time as epoch milliseconds."""
    return int(datetime.now(UTC).timestamp() * 1000)
