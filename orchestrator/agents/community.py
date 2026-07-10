"""Community agent: community announcement and queue stubs."""

from __future__ import annotations

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep


class CommunityAgent(BaseAgent):
    name = "community"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        if state.blocked:
            return state.record(self.skip(step, "skipped because a prior step blocked the run"))

        if step.requires_approval and not state.payload.get("approved"):
            return state.record(
                self.skip(step, "human approval required (pass approved=true to proceed)")
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

        queue = state.artifacts.setdefault("community_queue", [])
        queue.append(payload)

        if state.settings.dry_run:
            message = f"queued {action} (dry run)"
        else:
            message = f"would execute {action} (integration stub)"

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message=message,
                data=payload,
            )
        )
