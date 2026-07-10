"""Render the parameterized `{variable}` templates under `templates/`.

Templates use single-brace placeholders (e.g. `{game}`, `{release_date}`) so they read
naturally as plain markdown. Rendering substitutes any variables present in the context
and, by default, leaves unknown placeholders untouched so partial renders are safe.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping

_PLACEHOLDER = re.compile(r"\{([a-zA-Z0-9_]+)\}")

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def render(text: str, variables: Mapping[str, str], *, strict: bool = False) -> str:
    """Replace `{name}` placeholders in `text` using `variables`.

    When `strict` is True, an unknown placeholder raises KeyError; otherwise it is
    left in place so templates can be rendered in stages.
    """

    def _sub(match: re.Match[str]) -> str:
        name = match.group(1)
        if name in variables:
            return str(variables[name])
        if strict:
            raise KeyError(f"Unknown template variable: {name}")
        return match.group(0)

    return _PLACEHOLDER.sub(_sub, text)


def find_placeholders(text: str) -> set[str]:
    """Return the set of `{variable}` names referenced in `text`."""
    return set(_PLACEHOLDER.findall(text))


def render_file(
    relative_path: str, variables: Mapping[str, str], *, strict: bool = False
) -> str:
    """Load a template from `templates/` and render it with `variables`."""
    path = TEMPLATES_DIR / relative_path
    text = path.read_text(encoding="utf-8")
    return render(text, variables, strict=strict)
