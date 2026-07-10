"""Research agent: structured placeholders from game config and payload."""

from __future__ import annotations

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep


class ResearchAgent(BaseAgent):
    name = "research"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        game = state.settings.game
        facts = state.payload.get("facts", {})
        confirmed = facts.get("confirmed", [])
        unconfirmed = facts.get("unconfirmed", [])

        if not confirmed:
            confirmed = [
                f"{game.name} is tracked via official Rockstar channels.",
                f"Platforms of interest: {', '.join(game.platforms) or 'TBD'}.",
            ]

        research = {
            "game": game.name,
            "slug": game.slug,
            "release_date": game.release_date,
            "platforms": game.platforms,
            "official_sources": game.official_sources,
            "coverage_sources": game.coverage_sources,
            "confirmed_facts": confirmed,
            "unconfirmed_facts": unconfirmed,
            "content_tags": game.content_tags,
        }
        state.artifacts["research"] = research

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message="collected research placeholders",
                data={"confirmed_count": len(confirmed)},
            )
        )
