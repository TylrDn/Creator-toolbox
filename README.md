# Creator Toolbox

A game-agnostic operating system for creator-economy launches: content pipelines, community playbooks, product scaffolds, and a Python orchestrator that runs them offline with IP-safe defaults.

**Grand Theft Auto VI** is the first implementation target. The architecture stays configurable for future games via `config/games/*.yaml`.

## Why now

GTA 6 may drive one of the largest gaming attention cycles in years. Rockstar's Cfx.re/FiveM acquisition suggests user-generated server content has strategic value. Creator Toolbox gives you repeatable infrastructure before launch hype peaks, without betting on unverified marketplace details.

## Four business tracks

1. **Script products** — FiveM-compatible resources. **Custom job system (beta)** in [`scripts/custom-jobs/`](scripts/custom-jobs/).
2. **RP server business** — Design, moderation SOP, subscription tiers in `servers/`.
3. **AI NPC packs** — bartender, shopkeeper, quest giver configs + [`npc-packs/engine.py`](npc-packs/engine.py).
4. **Content + community + monetization engine** — Templates, YAML workflows, weekly run script.

## Repo structure

```text
Creator-toolbox/
  config/games/          # gta6.yaml, example.yaml
  docs/                  # Architecture, thesis, playbook, roadmap, FAQ
  templates/             # Parameterized markdown scaffolds
  orchestrator/        # YAML workflows, agents, CLI, integrations/
  scripts/               # Catalog, custom-jobs/, weekly_run.sh, tools/
  servers/               # RP server design, moderation, subscriptions
  npc-packs/             # NPC engine and configs
  playbooks/             # Shipping cadence per business track
  content/               # Calendar, KPI template, notes
  tests/                 # pytest suite (38 tests)
  .github/               # CI, Dependabot, issue/PR templates
```

## Getting started

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python -m orchestrator --list

python -m orchestrator gta6_news_drop \
  --var hook="Official update" \
  --var summary="New trailer on Rockstar Newswire" \
  --var news_type="trailer" \
  --var source="https://www.rockstargames.com/newswire" \
  --var cta="Join Discord" \
  --out --log

# Weekly content loop (calendar week 3 = product launch draft)
./scripts/weekly_run.sh 3

pytest tests/ -v --cov=orchestrator
```

Copy `.env.example` to `.env` for `GAME_SLUG`, `RELEASE_DATE`, and `DISCORD_WEBHOOK_URL`. Never commit `.env`.

### Add another game

Copy [`config/games/example.yaml`](config/games/example.yaml), edit fields, then:

```bash
python -m orchestrator gta6_news_drop --game your-slug --var summary="Update"
```

## How the orchestrator works

```text
research → drafting → critic → community / monetization / report
```

Workflows: `gta6_news_drop`, `product_launch`, `rp_server_launch`, `npc_pack_release`, `community_onboarding`, `weekly_report`.

- **dry run** (default): queues actions locally
- **`--live --approved`**: Discord webhook when `DISCORD_WEBHOOK_URL` is set; publish steps require approval
- **`--out --log`**: saves drafts and JSON run logs

## Roadmap

See [docs/roadmap.md](docs/roadmap.md). Phases 0–4 complete in repo; Phase 5 partial (Discord + report done; email analytics pending).

## Safety and IP policy

- Critic reviews all `--var` values and drafts before publish.
- No leaked builds, datamined assets, or re-hosted Rockstar art.

## Development workflow

1. Branch from `main`
2. Change code, docs, and tests together
3. `pytest tests/ -v`
4. Open a PR

## Status

**Operational v1.** Custom job system at beta, 6 workflows, 38 tests, Discord webhook optional. Run `./scripts/weekly_run.sh` for the human-in-the-loop content loop.

## License

MIT — see [LICENSE](LICENSE).
