"""Tests for report agent and integrations."""

from __future__ import annotations

from orchestrator.agents.base import RunState
from orchestrator.agents.report import ReportAgent
from orchestrator.integrations.discord import post_webhook
from orchestrator.models import WorkflowStep
from orchestrator.settings import load_settings


def test_report_agent_builds_summary() -> None:
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    state = RunState(workflow="weekly_report", settings=settings)
    state.steps.append(
        type("R", (), {"step_id": "x", "agent": "research", "status": "ok"})()
    )
    agent = ReportAgent()
    step = WorkflowStep(id="report", agent="report")
    result = agent.run(state, step)
    assert result.status == "ok"
    assert "report" in state.artifacts
    assert state.artifacts["report"]["game"] == "gta6"


def test_discord_webhook_skips_without_url(monkeypatch) -> None:
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    result = post_webhook("hello")
    assert result["ok"] is False
