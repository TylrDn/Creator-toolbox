"""Validate workflow definitions at load time."""

from __future__ import annotations

from pathlib import Path

from orchestrator.agents import AGENT_REGISTRY
from orchestrator.models import WorkflowDefinition
from orchestrator.templates import TEMPLATES_DIR


def validate_workflow(workflow: WorkflowDefinition) -> list[str]:
    """Return a list of validation errors (empty if valid)."""
    errors: list[str] = []

    if not workflow.steps:
        errors.append(f"workflow {workflow.name!r} has no steps")

    for step in workflow.steps:
        if step.agent not in AGENT_REGISTRY:
            errors.append(
                f"workflow {workflow.name!r} step {step.id!r}: unknown agent {step.agent!r}"
            )

        if step.template:
            template_path = TEMPLATES_DIR / step.template
            if not template_path.is_file():
                errors.append(
                    f"workflow {workflow.name!r} step {step.id!r}: "
                    f"template not found: {step.template!r}"
                )

    return errors


def validate_workflow_or_raise(workflow: WorkflowDefinition) -> None:
    errors = validate_workflow(workflow)
    if errors:
        raise ValueError("\n".join(errors))
