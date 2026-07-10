"""Tests for YAML workflow loading and router execution."""

from __future__ import annotations

import pytest

from orchestrator.router import Router, build_default_router, load_all_workflows, load_workflow
from orchestrator.settings import load_settings


def test_workflow_files_parse() -> None:
    workflows = load_all_workflows()
    expected = {"gta6_news_drop", "product_launch", "rp_server_launch", "npc_pack_release"}
    assert expected.issubset(set(workflows.keys()))
    for name, wf in workflows.items():
        assert wf.name == name
        assert len(wf.steps) >= 1


def test_gta6_news_drop_step_order() -> None:
    wf = load_workflow("orchestrator/workflows/gta6_news_drop.yaml")
    step_ids = [s.id for s in wf.steps]
    assert step_ids[0] == "research"
    assert "draft_discord" in step_ids
    assert "review_short" in step_ids


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
