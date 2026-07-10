"""Monetization agent: monetization suggestion payloads."""

from __future__ import annotations

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep


class MonetizationAgent(BaseAgent):
    name = "monetization"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        if state.blocked:
            return state.record(self.skip(step, "skipped because a prior step blocked the run"))

        content_type = step.content_type or step.extra.get("content_type", "short_video")
        categories = state.settings.game.monetization_categories

        suggestions = {
            "short_video": [
                "Affiliate links for capture gear and storage in description.",
                "Pin a Discord invite with a monetized setup guide.",
            ],
            "product_launch": [
                "Launch bundle with guide + overlay pack.",
                "Limited-time discount for email list subscribers.",
            ],
            "rp_server": [
                "Tiered subscription with cosmetic perks only.",
                "Whitelist priority pass as a one-time purchase.",
            ],
            "npc_pack": [
                "Per-pack license for server owners.",
                "Volume discount for multi-pack bundles.",
            ],
        }

        payload = {
            "content_type": content_type,
            "categories": categories,
            "suggestions": suggestions.get(content_type, suggestions["short_video"]),
            "dry_run": state.settings.dry_run,
        }

        state.artifacts.setdefault("monetization", []).append(payload)

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message=f"generated monetization suggestions for {content_type}",
                data=payload,
            )
        )
