"""Community agent: community announcement and queue stubs."""

from __future__ import annotations

import json
import time
from pathlib import Path

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.integrations.discord import post_webhook
from orchestrator.models import AgentResult, WorkflowStep
from orchestrator.utils import PROJECT_ROOT

OUTPUT_DIR = PROJECT_ROOT / "output"


class CommunityAgent(BaseAgent):
    name = "community"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        if state.blocked:
            return state.record(self.skip(step, "skipped because a prior step blocked the run"))

        if step.requires_approval and not state.payload.get("approved"):
            return state.record(
                self.skip(step, "human approval required (pass --approved to proceed)")
            )

        action = step.action or step.id
        drafts = state.artifacts.get("drafts", {})
        content = drafts.get(step.extra.get("source_step", "draft_discord"), drafts.get("draft_discord", ""))

        payload = {
            "action": action,
            "channel": state.settings.game.community_channels.get("discord_news", "#announcements"),
            "content_preview": content[:200] if content else "",
            "dry_run": state.settings.dry_run,
        }

        integration_result = None
        if not state.settings.dry_run and action in ("publish_discord", "queue_discord"):
            integration_result = post_webhook(content[:2000])
            payload["integration"] = integration_result

        if action == "queue_youtube":
            queue_path = self._write_youtube_queue(state, content, step)
            payload["youtube_queue_path"] = str(queue_path)

        queue = state.artifacts.setdefault("community_queue", [])
        queue.append(payload)

        if state.settings.dry_run:
            message = f"queued {action} (dry run)"
        elif integration_result and integration_result.get("ok"):
            message = f"executed {action} via Discord webhook"
        elif integration_result:
            message = f"integration failed for {action}: {integration_result.get('reason')}"
        else:
            message = f"queued {action}"

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message=message,
                data=payload,
            )
        )

    def _write_youtube_queue(self, state: RunState, content: str, step: WorkflowStep) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": int(time.time() * 1000),
            "workflow": state.workflow,
            "step_id": step.id,
            "title_hint": state.payload.get("variables", {}).get("hook", "Untitled"),
            "body_preview": content[:500],
            "status": "queued",
        }
        path = OUTPUT_DIR / "youtube-queue.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        return path
