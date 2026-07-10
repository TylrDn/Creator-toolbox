# Roadmap

Phased plan for Creator Toolbox. Status as of the rest-of-build pass.

## Phase 0: Repo bootstrap — complete

- Governance files, MIT license, contributing guide
- Directory layout for config, docs, templates, orchestrator, products
- GitHub CI skeleton and issue templates

**Exit criteria:** repo cloneable, tests run in CI, docs describe the system.

## Phase 1: Orchestrator MVP — complete

- YAML workflows and agent registry
- Game config loading (`config/games/gta6.yaml`)
- IP-safety critic with dry-run defaults
- CLI list/run/log commands

**Exit criteria:** four workflows run offline; critic blocks unsafe drafts in tests.

## Phase 1.5: Orchestrator hardening — complete

- Workflow validation at load time (`orchestrator/validation.py`)
- Unknown agent errors recorded as `error` steps
- CLI tests, settings/dotenv tests, `--approved` flag

## Phase 2: Product catalog and content engine — complete (beta)

- Script catalog and specs (`scripts/`)
- **Custom job system v1** in `scripts/custom-jobs/` (standalone, beta)
- Content calendar, KPI template, `scripts/weekly_run.sh`
- `community_onboarding` workflow
- `generate_lua.py` prompt builder

**Exit criteria:** one script spec end-to-end from catalog to shippable resource — met at beta.

## Phase 3: RP server operations — complete (docs)

- Server design and content pipeline docs
- `servers/moderation-sop.md`, `servers/subscription-tiers.md`
- `rp_server_launch` workflow available

**Exit criteria:** launch workflow produces Discord + short drafts — run locally with `--out`.

## Phase 4: AI NPC packs — complete

- `npc-packs/engine.py` local prompt builder
- Example configs: bartender, shopkeeper, quest_giver
- `npc_pack_release` workflow + tests

**Exit criteria:** NPC engine returns prompt payload without external API calls.

## Phase 5: Analytics and optimization — partial

- [x] KPI template (`content/kpi-template.yaml`)
- [x] Report agent + `weekly_report` workflow
- [x] Discord webhook adapter (`orchestrator/integrations/discord.py`)
- [x] YouTube metadata queue file (`output/youtube-queue.jsonl`)
- [ ] Email provider adapter
- [ ] Automated KPI ingestion from platform APIs
- [ ] A/B hook testing helpers

**Exit criteria:** weekly report artifact — met via `weekly_report` workflow + manual KPI YAML.

---

## Cross-cutting — complete

- `config/games/example.yaml` for game-agnostic swap demo
- 38 tests passing

## Next focus (operational, not repo)

1. Demo-server QA for `scripts/custom-jobs/`
2. Weekly content loop using `./scripts/weekly_run.sh`
3. First live Discord post: `--live --approved` with `DISCORD_WEBHOOK_URL` set
4. Ship job system beta listing + `product_launch` assets
