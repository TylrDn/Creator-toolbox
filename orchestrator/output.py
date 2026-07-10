"""Write rendered drafts to disk in a predictable, sortable layout."""

from __future__ import annotations

import re
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = _PROJECT_ROOT / "output"

_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Turn arbitrary text into a filesystem-safe slug."""
    slug = _SLUG.sub("-", value.lower()).strip("-")
    return slug or "draft"


def save_draft(
    event: str,
    content: str,
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    timestamp: int | None = None,
) -> Path:
    """Save `content` for an `event` and return the written path.

    Filenames are `<epoch_ms>-<event>.md` so runs sort chronologically and never collide.
    """
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    stamp = timestamp if timestamp is not None else int(time.time() * 1000)
    path = directory / f"{stamp}-{slugify(event)}.md"
    path.write_text(content, encoding="utf-8")
    return path
