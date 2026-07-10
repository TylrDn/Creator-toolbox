#!/usr/bin/env python3
"""Build an LLM prompt payload from a markdown product spec.

Does not call external APIs. Prints or saves the prompt for local use.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPEC = PROJECT_ROOT / "scripts" / "specs" / "job-system.md"


def load_spec(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_prompt(spec_text: str, *, target: str = "FiveM Lua resource") -> dict[str, str]:
    body = f"""You are implementing a {target} from the following product spec.

Requirements:
- Follow the spec structure and non-goals.
- Use clear module boundaries (client/server/shared).
- Include config validation and server-side payout checks.
- No external network calls in generated code.
- Add brief setup comments; avoid filler prose.

Product spec:
---
{spec_text}
---

Output: file list with brief purpose per file, then implementation for v1 core (config loader, clock in/out, single job task loop, payout).
"""
    return {"role": "user", "content": body}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC, help="path to markdown spec")
    parser.add_argument("--out", type=Path, default=None, help="write JSON prompt to file")
    parser.add_argument("--target", default="FiveM Lua resource", help="generation target label")
    args = parser.parse_args(argv)

    if not args.spec.exists():
        print(f"Spec not found: {args.spec}", file=sys.stderr)
        return 1

    payload = build_prompt(load_spec(args.spec), target=args.target)
    text = json.dumps(payload, indent=2)

    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote prompt -> {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
