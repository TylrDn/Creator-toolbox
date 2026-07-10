# Roadmap

Phased plan for Creator Toolbox. Phase 0 is largely complete in this first pass.

## Phase 0: Repo bootstrap

- Governance files, MIT license, contributing guide
- Directory layout for config, docs, templates, orchestrator, products
- GitHub CI skeleton and issue templates

**Exit criteria:** repo cloneable, tests run in CI, docs describe the system.

## Phase 1: Orchestrator MVP

- YAML workflows and agent registry
- Game config loading (`config/games/gta6.yaml`)
- IP-safety critic with dry-run defaults
- CLI list/run/log commands

**Exit criteria:** four workflows run offline; critic blocks unsafe drafts in tests.

## Phase 2: Product catalog and content engine

- Script catalog and specs (`scripts/`)
- Content calendar and notes (`content/`)
- Expanded template library and playbook docs
- `generate_lua.py` prompt builder for script development

**Exit criteria:** one script spec end-to-end from catalog to prompt output.

## Phase 3: RP server operations

- Server design and content pipeline docs (`servers/`)
- `rp_server_launch` workflow exercised with real template vars
- Subscription and moderation checklists in playbooks

**Exit criteria:** server launch workflow produces Discord + short-form drafts.

## Phase 4: AI NPC packs

- `npc-packs/engine.py` local prompt builder
- Example configs (bartender) and product doc
- `npc_pack_release` workflow wired to sales assets

**Exit criteria:** NPC engine returns prompt payload from YAML config without external API calls.

## Phase 5: Analytics and optimization

- KPI tracking templates and report agent (future)
- Integration adapters for YouTube, Discord, email analytics
- A/B hook testing helpers for short-form content

**Exit criteria:** weekly report artifact from aggregated metrics (when integrations exist).

---

Prioritize Phase 1 stability before expanding integrations. Keep each phase shippable on its own branch.
