"""Router: load YAML workflows, run agents sequentially, capture run logs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from orchestrator.agents import build_agent
from orchestrator.agents.base import RunState
from orchestrator.models import AgentResult, RunLogEntry, Settings, WorkflowDefinition, WorkflowStep
from orchestrator.utils import epoch_ms, load_yaml, utc_timestamp
from orchestrator.validation import validate_workflow_or_raise

LOGS_DIR = Path(__file__).resolve().parent / "logs"
WORKFLOWS_DIR = Path(__file__).resolve().parent / "workflows"


def _parse_step(raw: dict[str, Any]) -> WorkflowStep:
    return WorkflowStep(
        id=str(raw["id"]),
        agent=str(raw["agent"]),
        template=raw.get("template"),
        action=raw.get("action"),
        review_step=raw.get("review_step"),
        content_type=raw.get("content_type"),
        retries=int(raw.get("retries", 0)),
        requires_approval=bool(raw.get("requires_approval", False)),
        extra=dict(raw.get("extra", {})),
    )


def load_workflow(path: str | Path) -> WorkflowDefinition:
    """Load a single workflow YAML file."""
    data = load_yaml(path)
    steps = [_parse_step(step) for step in data.get("steps", [])]
    workflow = WorkflowDefinition(
        name=str(data.get("name", Path(path).stem)),
        description=str(data.get("description", "")),
        steps=steps,
    )
    validate_workflow_or_raise(workflow)
    return workflow


def load_all_workflows(directory: str | Path | None = None) -> dict[str, WorkflowDefinition]:
    """Load every *.yaml workflow from the workflows directory."""
    folder = Path(directory) if directory else WORKFLOWS_DIR
    workflows: dict[str, WorkflowDefinition] = {}
    for path in sorted(folder.glob("*.yaml")):
        workflow = load_workflow(path)
        workflows[workflow.name] = workflow
    return workflows


@dataclass
class RunSummary:
    """High-level outcome of a workflow run."""

    workflow: str
    blocked: bool
    steps: list[AgentResult]
    artifacts: dict[str, Any]
    log_path: Path | None = None


@dataclass
class Router:
    """Registry of workflow name -> definition, plus the run loop."""

    workflows: dict[str, WorkflowDefinition] = field(default_factory=dict)

    @classmethod
    def from_directory(cls, directory: str | Path | None = None) -> Router:
        return cls(workflows=load_all_workflows(directory))

    def run(
        self,
        workflow_name: str,
        settings: Settings,
        payload: dict[str, Any] | None = None,
        *,
        write_log: bool = False,
    ) -> RunSummary:
        if workflow_name not in self.workflows:
            raise KeyError(f"No workflow registered for: {workflow_name!r}")

        workflow = self.workflows[workflow_name]
        state = RunState(workflow=workflow_name, settings=settings, payload=payload or {})
        log_entries: list[RunLogEntry] = []

        for step in workflow.steps:
            result = self._execute_step(state, step)
            log_entries.append(
                RunLogEntry(
                    timestamp=utc_timestamp(),
                    workflow=workflow_name,
                    step_id=step.id,
                    agent=step.agent,
                    status=result.status,
                    message=result.message,
                )
            )

        log_path = None
        if write_log:
            log_path = self._write_log(workflow_name, state, log_entries)

        state.artifacts["summary"] = {
            "workflow": workflow_name,
            "game": settings.game.slug,
            "blocked": state.blocked,
            "step_count": len(state.steps),
            "dry_run": settings.dry_run,
        }

        return RunSummary(
            workflow=workflow_name,
            blocked=state.blocked,
            steps=state.steps,
            artifacts=state.artifacts,
            log_path=log_path,
        )

    def _execute_step(self, state: RunState, step: WorkflowStep) -> AgentResult:
        try:
            agent = build_agent(step.agent)
        except KeyError as exc:
            result = AgentResult(
                agent=step.agent,
                step_id=step.id,
                status="error",
                message=str(exc),
            )
            state.steps.append(result)
            return result

        attempts = step.retries + 1
        last_result: AgentResult | None = None

        for attempt in range(attempts):
            try:
                result = agent.run(state, step)
            except Exception as exc:  # noqa: BLE001 - capture for run log
                result = AgentResult(
                    agent=step.agent,
                    step_id=step.id,
                    status="error",
                    message=str(exc),
                )
                state.steps.append(result)

            last_result = result
            if result.status != "error":
                return result

        assert last_result is not None
        return last_result

    def _write_log(
        self,
        workflow_name: str,
        state: RunState,
        entries: list[RunLogEntry],
    ) -> Path:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        record = {
            "workflow": workflow_name,
            "game": state.settings.game.slug,
            "blocked": state.blocked,
            "timestamp": utc_timestamp(),
            "steps": [
                {
                    "step_id": entry.step_id,
                    "agent": entry.agent,
                    "status": entry.status,
                    "message": entry.message,
                }
                for entry in entries
            ],
        }
        path = LOGS_DIR / f"{epoch_ms()}-{workflow_name}.json"
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        return path


def build_default_router() -> Router:
    """Load workflows from the default directory."""
    return Router.from_directory()


__all__ = ["Router", "RunSummary", "build_default_router", "load_all_workflows", "load_workflow"]
