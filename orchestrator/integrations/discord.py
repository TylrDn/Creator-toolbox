"""Discord webhook integration (optional, env-driven)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def post_webhook(content: str, *, webhook_url: str | None = None) -> dict:
    """Post content to a Discord webhook. Returns result metadata."""
    url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not url:
        return {"ok": False, "reason": "DISCORD_WEBHOOK_URL not set"}

    payload = json.dumps({"content": content[:2000]}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Creator-Toolbox-Orchestrator"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return {"ok": True, "status": response.status}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "reason": f"HTTP {exc.code}", "body": exc.read().decode()[:200]}
    except urllib.error.URLError as exc:
        return {"ok": False, "reason": str(exc.reason)}
