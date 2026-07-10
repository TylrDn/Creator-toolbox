"""Tests for individual agents."""

from __future__ import annotations

from orchestrator.agents.base import RunState
from orchestrator.agents.critic import CriticAgent
from orchestrator.agents.drafting import DraftingAgent
from orchestrator.models import WorkflowStep
from orchestrator.settings import load_settings


def _state_with_draft(draft_text: str, step_id: str = "draft_short") -> RunState:
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    state = RunState(workflow="test", settings=settings)
    state.artifacts["drafts"] = {step_id: draft_text}
    state.artifacts["latest_draft"] = draft_text
    return state


def test_critic_blocks_leak_language() -> None:
    agent = CriticAgent()
    state = _state_with_draft("This leaked build shows new mechanics.")
    step = WorkflowStep(id="review_short", agent="critic", review_step="draft_short")
    result = agent.run(state, step)
    assert result.status == "blocked"
    assert state.blocked is True
    assert "leaked" in result.message.lower() or "leak" in result.message.lower()


def test_critic_passes_clean_draft() -> None:
    agent = CriticAgent()
    state = _state_with_draft("Grand Theft Auto VI trailer discussed using official sources.")
    step = WorkflowStep(id="review_short", agent="critic", review_step="draft_short")
    result = agent.run(state, step)
    assert result.status == "ok"
    assert not state.blocked


def test_critic_passes_clean_discord_draft() -> None:
    """Discord template IP reminder mentions 'leaked'; must not false-positive."""
    agent = CriticAgent()
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    state = RunState(
        workflow="test",
        settings=settings,
        payload={"variables": {"summary": "Official trailer looks great"}},
    )
    state.artifacts["drafts"] = {
        "draft_discord": (
            "**Body:**\n> Official trailer looks great\n\n"
            "**IP Safety Reminder:**\n- Do **not** post leaked footage.\n"
        ),
    }
    step = WorkflowStep(
        id="review_assets",
        agent="critic",
        extra={"review_drafts": "all"},
    )
    result = agent.run(state, step)
    assert result.status == "ok"
    assert not state.blocked


def test_critic_blocks_leak_in_payload_variables() -> None:
    """Leaks in summary must block even when short-video draft is clean."""
    agent = CriticAgent()
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    state = RunState(
        workflow="test",
        settings=settings,
        payload={"variables": {"hook": "Clean hook", "summary": "This leaked build is bad"}},
    )
    state.artifacts["drafts"] = {
        "draft_short": "Clean short content with hook: Clean hook",
        "draft_discord": "> Clean hook\n**IP Safety Reminder:**\n- Do **not** post leaked footage.",
    }
    step = WorkflowStep(
        id="review_assets",
        agent="critic",
        extra={"review_drafts": "all"},
    )
    result = agent.run(state, step)
    assert result.status == "blocked"
    assert state.blocked is True


def test_drafting_renders_template() -> None:
    settings = load_settings(game_slug="gta6", use_dotenv=False)
    settings.extra = {"hook": "Countdown", "cta": "Subscribe"}
    state = RunState(workflow="test", settings=settings, payload={"variables": settings.extra})
    step = WorkflowStep(
        id="draft_short",
        agent="drafting",
        template="content/short-video.md",
    )
    agent = DraftingAgent()
    result = agent.run(state, step)
    assert result.status == "ok"
    assert "draft_short" in state.artifacts["drafts"]
    assert "Grand Theft Auto VI" in state.artifacts["drafts"]["draft_short"]
