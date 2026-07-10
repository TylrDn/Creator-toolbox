"""Critic agent: IP-safety review before publish steps."""

from __future__ import annotations

import re

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep

DEFAULT_BANNED_PATTERNS = [
    r"leak(?:ed|s)?",
    r"datamin(?:e|ed|ing)",
    r"data\s*mine",
    r"pirat(?:e|ed|ing)",
    r"cracked\s+copy",
    r"torrent",
    r"early\s+copy",
    r"stolen\s+(?:build|footage|assets?)",
    r"re-?hosted\s+(?:art|assets?|logo)",
]


class CriticAgent(BaseAgent):
    name = "critic"

    def __init__(self, banned_patterns: list[str] | None = None) -> None:
        patterns = banned_patterns if banned_patterns is not None else DEFAULT_BANNED_PATTERNS
        self._regexes = [re.compile(rf"\b{p}\b", re.IGNORECASE) for p in patterns]

    def review(self, text: str) -> list[str]:
        """Return banned phrases found in text."""
        violations: list[str] = []
        for regex in self._regexes:
            match = regex.search(text)
            if match:
                violations.append(match.group(0).lower())
        return violations

    def _resolve_draft(self, state: RunState, step: WorkflowStep) -> str:
        drafts = state.artifacts.get("drafts", {})
        review_key = step.review_step or step.id.replace("review_", "draft_")
        if review_key in drafts:
            return drafts[review_key]
        return state.artifacts.get("latest_draft", "")

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        ip_rules = state.settings.game.ip_safety
        if not ip_rules.get("forbid_leaks", True):
            return state.record(
                AgentResult(
                    agent=self.name,
                    step_id=step.id,
                    status="ok",
                    message="IP review skipped (forbid_leaks disabled)",
                )
            )

        patterns = ip_rules.get("banned_patterns")
        if patterns:
            regexes = [re.compile(rf"\b{p}\b", re.IGNORECASE) for p in patterns]
        else:
            regexes = self._regexes

        draft = self._resolve_draft(state, step)
        violations: list[str] = []
        for regex in regexes:
            match = regex.search(draft)
            if match:
                violations.append(match.group(0).lower())

        if violations:
            unique = sorted(set(violations))
            state.artifacts["ip_violations"] = unique
            return state.record(
                AgentResult(
                    agent=self.name,
                    step_id=step.id,
                    status="blocked",
                    message="IP-safety block: " + ", ".join(unique),
                    data={"violations": unique},
                )
            )

        state.artifacts.setdefault("approved_steps", []).append(step.review_step or step.id)
        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message="passed IP-safety review",
            )
        )
