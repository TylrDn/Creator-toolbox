"""Drafting agent: render markdown templates into structured draft payloads."""

from __future__ import annotations

from orchestrator import templates
from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep


class DraftingAgent(BaseAgent):
    name = "drafting"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        if not step.template:
            return state.record(
                AgentResult(
                    agent=self.name,
                    step_id=step.id,
                    status="error",
                    message="drafting step requires a template path",
                )
            )

        variables = dict(state.settings.as_variables())
        for key, value in state.payload.get("variables", {}).items():
            variables[key] = str(value)

        rendered = templates.render_file(step.template, variables)
        unresolved = sorted(templates.find_placeholders(rendered))

        drafts = state.artifacts.setdefault("drafts", {})
        drafts[step.id] = rendered
        state.artifacts["latest_draft"] = rendered

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message=f"rendered {step.template}"
                + (f"; unresolved: {', '.join(unresolved)}" if unresolved else ""),
                data={"template": step.template, "unresolved": unresolved},
            )
        )
