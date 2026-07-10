"""Agent base types and shared run state."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from orchestrator.models import AgentResult, Settings, WorkflowStep


@dataclass
class RunState:
    """Mutable state threaded through every agent in a workflow run."""

    workflow: str
    settings: Settings
    payload: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)
    steps: list[AgentResult] = field(default_factory=list)
    blocked: bool = False

    def record(self, result: AgentResult) -> AgentResult:
        self.steps.append(result)
        if result.status == "blocked":
            self.blocked = True
        return result


class BaseAgent(ABC):
    """Base class for workflow agents."""

    name: str = "agent"

    @abstractmethod
    def run(self, state: RunState, step: WorkflowStep) -> AgentResult:
        ...

    def skip(self, step: WorkflowStep, message: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            step_id=step.id,
            status="skipped",
            message=message,
        )
