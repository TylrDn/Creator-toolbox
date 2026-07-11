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

# Template boilerplate that mentions banned words in a negation/reminder context.
# Matches both "**IP Safety Reminder:**" (inline bold) and "## IP Safety" (section heading).
# Terminates at the next markdown section (##), horizontal rule (---), or end of string.
_BOILERPLATE_SECTION = re.compile(
    r"(?:\*\*IP Safety(?:\s+Reminder)?:\*\*|##\s+IP Safety\b).*?(?=\n##\s|\n---\s*\n|\Z)",
    re.DOTALL | re.IGNORECASE,
)


def _strip_boilerplate(text: str) -> str:
    """Remove template IP-safety sections that mention banned words in negation."""
    return _BOILERPLATE_SECTION.sub("", text)


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

    def _compile_regexes(self, state: RunState) -> list[re.Pattern[str]]:
        ip_rules = state.settings.game.ip_safety
        patterns = ip_rules.get("banned_patterns")
        if patterns:
            return [re.compile(rf"\b{p}\b", re.IGNORECASE) for p in patterns]
        return self._regexes

    def _gather_review_texts(self, state: RunState, step: WorkflowStep) -> list[str]:
        """Collect user variables and draft bodies to scan."""
        texts: list[str] = []

        for value in state.payload.get("variables", {}).values():
            if isinstance(value, str) and value.strip():
                texts.append(value)

        drafts = state.artifacts.get("drafts", {})
        review_drafts = step.extra.get("review_drafts")
        if review_drafts == "all":
            keys = list(drafts.keys())
        elif isinstance(review_drafts, list):
            keys = list(review_drafts)
        elif step.review_step:
            keys = [step.review_step]
        else:
            fallback = step.id.replace("review_", "draft_")
            keys = [fallback] if fallback in drafts else []

        for key in keys:
            if key in drafts:
                texts.append(_strip_boilerplate(drafts[key]))

        return texts

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

        regexes = self._compile_regexes(state)
        review_texts = self._gather_review_texts(state, step)

        violations: list[str] = []
        for text in review_texts:
            for regex in regexes:
                match = regex.search(text)
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
