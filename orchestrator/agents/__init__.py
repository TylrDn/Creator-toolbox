"""Agents that compose into YAML-defined workflows."""

from orchestrator.agents.base import BaseAgent, RunState
from orchestrator.agents.community import CommunityAgent
from orchestrator.agents.critic import CriticAgent
from orchestrator.agents.drafting import DraftingAgent
from orchestrator.agents.monetization import MonetizationAgent
from orchestrator.agents.report import ReportAgent
from orchestrator.agents.research import ResearchAgent
from orchestrator.models import AgentResult

AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    "research": ResearchAgent,
    "drafting": DraftingAgent,
    "critic": CriticAgent,
    "community": CommunityAgent,
    "monetization": MonetizationAgent,
    "report": ReportAgent,
}


def build_agent(name: str) -> BaseAgent:
    """Instantiate an agent by registry name."""
    if name not in AGENT_REGISTRY:
        raise KeyError(f"Unknown agent: {name!r}")
    return AGENT_REGISTRY[name]()


__all__ = [
    "AGENT_REGISTRY",
    "AgentResult",
    "BaseAgent",
    "CommunityAgent",
    "CriticAgent",
    "DraftingAgent",
    "MonetizationAgent",
    "ReportAgent",
    "ResearchAgent",
    "RunState",
    "build_agent",
]
