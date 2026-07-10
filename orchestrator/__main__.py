"""CLI entrypoint: run a YAML workflow.

Examples:
    python -m orchestrator --list
    python -m orchestrator gta6_news_drop
    python -m orchestrator gta6_news_drop --var hook="Countdown" --var cta="Join Discord"
"""

from __future__ import annotations

import argparse
import json
import sys

from orchestrator import output
from orchestrator.router import build_default_router
from orchestrator.settings import load_settings


def _parse_vars(pairs: list[str]) -> dict[str, str]:
    variables: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"--var expects key=value, got: {pair!r}")
        key, value = pair.split("=", 1)
        variables[key.strip()] = value
    return variables


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orchestrator", description=__doc__)
    parser.add_argument("workflow", nargs="?", help="workflow to run (e.g. gta6_news_drop)")
    parser.add_argument("--list", action="store_true", help="list available workflows")
    parser.add_argument(
        "--game",
        default=None,
        help="game config slug (default: gta6 or GAME_SLUG env)",
    )
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="template variable override (repeatable)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="disable dry_run (integration stubs only in this pass)",
    )
    parser.add_argument(
        "--out",
        action="store_true",
        help="save the latest draft to the output/ directory",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="write a JSON run log to orchestrator/logs/",
    )
    parser.add_argument(
        "--approved",
        action="store_true",
        help="mark run as human-approved for requires_approval steps",
    )
    args = parser.parse_args(argv)

    router = build_default_router()

    if args.list or not args.workflow:
        print("Available workflows:")
        for name, wf in router.workflows.items():
            print(f"  {name:22} {wf.description}")
        return 0

    settings = load_settings(game_slug=args.game, dry_run=not args.live, extra=_parse_vars(args.var))
    payload: dict = {"variables": _parse_vars(args.var)}
    if args.approved:
        payload["approved"] = True
    summary = router.run(args.workflow, settings, payload, write_log=args.log)

    if args.out and not summary.blocked:
        draft = summary.artifacts.get("latest_draft", "")
        path = output.save_draft(args.workflow, draft)
        print(f"saved draft -> {path}", file=sys.stderr)

    print(json.dumps(summary.artifacts.get("summary", {}), indent=2))
    return 1 if summary.blocked else 0


if __name__ == "__main__":
    sys.exit(main())
