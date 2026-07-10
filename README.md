# Creator Toolbox

A game-agnostic operating system for creator-economy launches: content pipelines, community playbooks, product scaffolds, and a Python orchestrator that runs them offline with IP-safe defaults.

**Grand Theft Auto VI** is the first implementation target. The architecture stays configurable for future games via `config/games/*.yaml`.

## Why now

GTA 6 may drive one of the largest gaming attention cycles in years. Rockstar's Cfx.re/FiveM acquisition suggests user-generated server content has strategic value. Creator Toolbox gives you repeatable infrastructure before launch hype peaks, without betting on unverified marketplace details.

## Four business tracks

1. **Script products** — FiveM-compatible resources (jobs, economy, UI). Catalog and specs in `scripts/`.
2. **RP server business** — Server design, content pipeline, and launch workflows in `servers/` and `playbooks/rp-server.md`.
3. **AI NPC packs** — Role configs and a local prompt engine in `npc-packs/`.
4. **Content + community + monetization engine** — Templates, YAML workflows, and the orchestrator tie the other tracks together.

## Repo structure

```text
Creator-toolbox/
  config/games/gta6.yaml       # Game config, IP rules, channels
  docs/                        # Architecture, thesis, playbook, roadmap, FAQ
  templates/                   # Parameterized markdown scaffolds
  orchestrator/                # YAML workflows, agents, CLI
  scripts/                     # Product catalog, specs, tools
  servers/                     # RP server design and content pipeline
  npc-packs/                   # NPC engine and example configs
  playbooks/                   # Shipping cadence per business track
  content/                     # Calendar and research notes
  tests/                       # pytest suite
  .github/                     # CI, Dependabot, issue/PR templates
```

## Getting started

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# List workflows
python -m orchestrator --list

# Run a news-drop pipeline (dry run, nothing published)
python -m orchestrator gta6_news_drop \
  --var hook="Official update" \
  --var summary="New trailer on Rockstar Newswire" \
  --var news_type="trailer" \
  --var source="https://www.rockstargames.com/newswire" \
  --var cta="Join Discord"

# Save latest draft and write a run log
python -m orchestrator gta6_news_drop --var hook="Test" --out --log

# Run tests
pytest tests/ -v --cov=orchestrator
```

Copy `.env.example` to `.env` for optional overrides (`GAME_SLUG`, `RELEASE_DATE`, integration keys). Never commit `.env`.

## How the orchestrator works

Workflows are YAML files in `orchestrator/workflows/`. Each step calls an agent:

```text
research → drafting → critic → community / monetization
```

- **research** — structured placeholders from game config
- **drafting** — renders templates from `templates/`
- **critic** — blocks leak/datamine/piracy language when `ip_safety.forbid_leaks` is true
- **community** — queues Discord/YouTube/email actions (stubbed; honors dry run)
- **monetization** — attaches monetization suggestions by content type

Runs default to **dry run**. Pass `--live` for integration stubs only (no real API calls in this pass).

Available workflows: `gta6_news_drop`, `product_launch`, `rp_server_launch`, `npc_pack_release`.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md). Phases 0–1 (repo bootstrap + orchestrator MVP) are largely complete. Phase 2+ adds real integrations, analytics, and expanded product catalogs.

## Safety and IP policy

- Use official sources; label speculation.
- Critic agent enforces per-game `ip_safety` rules in config.
- No leaked builds, datamined assets, or re-hosted Rockstar art in templates or examples.
- See [docs/gta6-creator-economy-thesis.md](docs/gta6-creator-economy-thesis.md) for strategic risks.

## Development workflow

1. Branch from `main`: `feat/your-feature`
2. Change code, docs, and tests together
3. Run `pytest tests/ -v`
4. Open a PR using the template

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) for contributor and AI-agent conventions.

## Status

**Early but operational.** The orchestrator runs four workflows offline, tests pass in CI, and product modules are documented scaffolds. External publish integrations are stubbed for a later phase.

## License

MIT — see [LICENSE](LICENSE).
