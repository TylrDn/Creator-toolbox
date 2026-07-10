# Agent / AI context

## Project

- **Purpose**: Repeatable, game-agnostic infrastructure for creator-economy launches (content, community, monetization, scripts, RP servers, NPC packs), starting with GTA 6.
- **Stack**: Python 3.11+, PyYAML for config/workflows, pytest for tests. Markdown scaffolds under `docs/`, `templates/`, `playbooks/`.
- **How to run**: `python -m orchestrator --list`, then e.g. `python -m orchestrator gta6_news_drop --var hook="Countdown"`.
- **How to test**: `pytest tests/ --cov=orchestrator`.
- **How to lint / typecheck**: no linter configured yet; follow PEP 8 and add type hints.

### Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ --cov=orchestrator
```

> Environment note: inside the Cursor AppImage terminal, Python's `sys.executable`
> can be misreported (venv symlinks/`sys.executable` resolve to the AppImage). Use a
> normal system terminal for venv work, or run Python via a sanitized environment
> (`env -i HOME="$HOME" PATH=/usr/bin:/bin ./venv/bin/python ...`).

## Conventions for AI changes

- Prefer the smallest diff that solves the task; avoid drive-by refactors.
- Follow existing naming, formatting, and template patterns.
- Templates use `{curly_braces}` variables (e.g. `{game}`, `{release_date}`, `{platforms}`).
- IP-safe by default: no leaks, datamining, or re-hosted copyrighted assets.
- Never commit secrets; use `.env` (documented in README and ignored via `.gitignore`).
- Use conventional commits (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`).
- After substantive edits: run the same checks CI runs (tests) before considering work done.

## Repo map

- `config/games/` — per-game YAML (sources, IP rules, channels)
- `docs/` — architecture, thesis, playbook, roadmap, FAQ
- `templates/` — content, community, monetization markdown scaffolds
- `orchestrator/` — `models.py`, `settings.py`, `router.py`, `utils.py`, `agents/`, `workflows/*.yaml`, CLI
- `scripts/` — product catalog, specs, `generate_lua.py`
- `servers/` — RP server design and content pipeline
- `npc-packs/` — NPC prompt engine and configs
- `playbooks/` — per-track shipping guides
- `content/` — calendar and notes
- `tests/` — pytest suite

## Orchestrator model

- A **workflow** is a YAML file listing ordered **steps** with an `agent` field.
- Agents: `research`, `drafting`, `critic`, `community`, `monetization`.
- The **router** loads workflows, runs steps sequentially, supports retries, and writes optional JSON logs.
- The **critic** enforces IP-safety from `config/games/*.yaml`. Blocked runs skip publish-style steps but keep the audit trail.
- **Safety defaults**: `Settings.dry_run` is `True` unless `--live` is passed.
- Add a workflow by creating `orchestrator/workflows/<name>.yaml`.
