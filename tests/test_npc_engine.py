"""Tests for the NPC pack engine."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

NPC_ROOT = Path(__file__).resolve().parent.parent / "npc-packs"
_spec = importlib.util.spec_from_file_location("npc_engine", NPC_ROOT / "engine.py")
assert _spec and _spec.loader
npc_engine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(npc_engine)


def test_load_bartender_config() -> None:
    cfg = npc_engine.load_npc_config(NPC_ROOT / "config" / "bartender.yaml")
    assert cfg["id"] == "bartender"
    assert cfg["role"] == "bartender"


def test_build_prompt_includes_context() -> None:
    cfg = npc_engine.load_npc_config(NPC_ROOT / "config" / "shopkeeper.yaml")
    prompt = npc_engine.build_prompt(cfg, player_history=["bought bait"], context="Morning at the shop.")
    assert "shopkeeper" in prompt["system"].lower()
    assert "Morning at the shop" in prompt["user"]
    assert "bought bait" in prompt["user"]


def test_all_example_configs_load() -> None:
    for name in ("bartender", "shopkeeper", "quest_giver"):
        path = NPC_ROOT / "config" / f"{name}.yaml"
        cfg = npc_engine.load_npc_config(path)
        assert cfg["id"] == name
        assert cfg.get("safety_boundaries")


def test_missing_config_raises() -> None:
    with pytest.raises((FileNotFoundError, ValueError)):
        npc_engine.load_npc_config(NPC_ROOT / "config" / "missing.yaml")
