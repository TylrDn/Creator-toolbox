"""Core data models for config, workflows, and run logs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GameConfig:
    """Game-specific configuration loaded from config/games/*.yaml."""

    slug: str
    name: str
    release_date: str
    platforms: list[str]
    official_sources: list[str]
    coverage_sources: list[str]
    ip_safety: dict[str, Any]
    content_tags: list[str]
    community_channels: dict[str, str]
    monetization_categories: list[str]

    def as_variables(self) -> dict[str, str]:
        """Flatten game config into template variables."""
        return {
            "game": self.name,
            "release_date": self.release_date,
            "platforms": ", ".join(self.platforms),
        }


@dataclass
class Settings:
    """Runtime settings for a workflow run."""

    game: GameConfig
    dry_run: bool = True
    extra: dict[str, Any] = field(default_factory=dict)

    def as_variables(self) -> dict[str, str]:
        variables = self.game.as_variables()
        for key, value in self.extra.items():
            variables[key] = str(value)
        return variables


@dataclass
class AgentResult:
    """Outcome of a single agent step."""

    agent: str
    step_id: str
    status: str  # ok | blocked | skipped | error
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStep:
    """One step in a YAML-defined workflow."""

    id: str
    agent: str
    template: str | None = None
    action: str | None = None
    review_step: str | None = None
    content_type: str | None = None
    retries: int = 0
    requires_approval: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDefinition:
    """A named workflow loaded from YAML."""

    name: str
    description: str
    steps: list[WorkflowStep]


@dataclass
class RunLogEntry:
    """Structured log line for a completed step."""

    timestamp: str
    workflow: str
    step_id: str
    agent: str
    status: str
    message: str
