"""Report agent: weekly KPI summary from manual template."""

from __future__ import annotations

from pathlib import Path

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.models import AgentResult, WorkflowStep
from orchestrator.utils import PROJECT_ROOT, load_yaml, utc_timestamp


class ReportAgent(BaseAgent):
    name = "report"

    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        kpi_path = Path(step.extra.get("kpi_path", PROJECT_ROOT / "content" / "kpi-template.yaml"))
        metrics: dict = {}
        if kpi_path.exists():
            raw = load_yaml(kpi_path)
            metrics = {
                "week": raw.get("week"),
                "metrics": raw.get("metrics", {}),
            }

        report = {
            "timestamp": utc_timestamp(),
            "workflow": state.workflow,
            "game": state.settings.game.slug,
            "blocked": state.blocked,
            "step_summary": [
                {"step_id": s.step_id, "agent": s.agent, "status": s.status}
                for s in state.steps
            ],
            "kpi": metrics,
            "community_queue_count": len(state.artifacts.get("community_queue", [])),
            "monetization_count": len(state.artifacts.get("monetization", [])),
        }

        state.artifacts["report"] = report

        return state.record(
            AgentResult(
                agent=self.name,
                step_id=step.id,
                status="ok",
                message="generated run report",
                data={"report_keys": list(report.keys())},
            )
        )
