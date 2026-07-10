"""Tests for YAML workflow loading and router execution."""

from __future__ import annotations

import pytest

from orchestrator.models import WorkflowDefinition, WorkflowStep
from orchestrator.router import Router, build_default_router, load_all_workflows, load_workflow
from orchestrator.settings import load_settings
from orchestrator.validation import validate_workflow


def test_workflow_files_parse() -> None:
    workflows = load_all_workflows()
    expected = {"gta6_news_drop", "product_launch", "rp_server_launch", "npc_pack_release", "community_onboarding", "weekly_report"}
    assert expected.issubset(set(workflows.keys()))
    for name, wf in workflows.items():
        assert wf.name == name
        assert len(wf.steps) >= 1


def test_gta6_news_drop_step_order() -> None:
    wf = load_workflow("orchestrator/workflows/gta6_news_drop.yaml")
    step_ids = [s.id for s in wf.steps]
    assert step_ids[0] == "research"
    assert "draft_discord" in step_ids
    assert "review_assets" in step_ids
    review_idx = step_ids.index("review_assets")
    assert review_idx > step_ids.index("draft_discord")
    assert review_idx > step_ids.index("draft_short")
    assert review_idx < step_ids.index("publish_discord")


def test_gta6_news_drop_blocks_leak_in_summary() -> None:
    router = build_default_router()
    settings = load_settings(game_slug="gta6", dry_run=True, use_dotenv=False)
    payload = {
        "variables": {
            "hook": "Clean hook",
            "summary": "This leaked build is amazing",
            "news_type": "trailer",
            "source": "https://www.rockstargames.com/newswire",
            "cta": "Join Discord",
        }
    }
    summary = router.run("gta6_news_drop", settings, payload)
    assert summary.blocked is True
    publish_steps = [s for s in summary.steps if s.agent == "community" and s.status == "ok"]
    assert publish_steps == []


def test_router_executes_workflow_without_crashing() -> None:
    router = build_default_router()
    settings = load_settings(game_slug="gta6", dry_run=True, use_dotenv=False)
    payload = {
        "variables": {
            "hook": "Test hook",
            "cta": "Join Discord",
            "summary": "Official update",
            "news_type": "trailer",
            "source": "https://www.rockstargames.com/newswire",
        }
    }
    summary = router.run("gta6_news_drop", settings, payload)
    assert summary.workflow == "gta6_news_drop"
    assert len(summary.steps) == len(router.workflows["gta6_news_drop"].steps)
    assert "research" in summary.artifacts
    assert "drafts" in summary.artifacts


def test_unknown_workflow_raises() -> None:
    router = Router(workflows={})
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    with pytest.raises(KeyError):
        router.run("does_not_exist", settings, {})


def test_unknown_agent_records_error_step() -> None:
    bad = WorkflowDefinition(
        name="bad_agent_test",
        description="test",
        steps=[WorkflowStep(id="bad", agent="nonexistent")],
    )
    router = Router(workflows={"bad_agent_test": bad})
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    summary = router.run("bad_agent_test", settings, {})
    assert summary.steps[0].status == "error"
    assert "Unknown agent" in summary.steps[0].message


def test_validate_workflow_catches_bad_template() -> None:
    wf = WorkflowDefinition(
        name="bad_template",
        description="test",
        steps=[
            WorkflowStep(id="d", agent="drafting", template="does/not/exist.md"),
        ],
    )
    errors = validate_workflow(wf)
    assert any("template not found" in e for e in errors)
