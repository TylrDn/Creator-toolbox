# FAQ

## Is this easy money?

No. Creator economies reward consistent shipping, moderation, and product quality. Most projects fail on execution or platform policy changes, not lack of ideas.

## Why GTA 6?

Large audience, long pre-launch runway, and Rockstar's FiveM signal make it a strong first test case for scripts, RP servers, NPC packs, and content pipelines. The repo stays game-agnostic via config.

## Why not just stream?

Streaming is one channel. This repo also covers products (scripts, NPC packs), server subscriptions, email, and repeatable workflows. Streaming can feed those businesses without being the only revenue line.

## Why use AI agents?

Agents here are small, auditable steps (research, draft, review, queue), not autonomous swarms. They standardize launch pipelines and enforce IP checks so you spend time on judgment calls, not copy-paste.

## How do we stay compliant?

- Use official sources and label speculation.
- Run the critic agent; it blocks leak/datamine/piracy language when configured.
- Read Rockstar terms and game-specific `ip_safety` rules in `config/games/`.
- Do not commit secrets; use `.env` for API keys.

## Can this expand to other games?

Yes. Add `config/games/<slug>.yaml`, copy or adapt workflows, and swap templates. The orchestrator does not hard-code GTA 6.

## Are integrations production-ready?

Not in this pass. Community and publish steps are stubs that honor `dry_run`. Real API adapters are planned for Phase 5.

## Where do I start?

```bash
pip install -r requirements.txt
python -m orchestrator --list
python -m orchestrator gta6_news_drop --var hook="News drop" --var summary="Official update"
pytest tests/ -v
```

See `README.md` for the full layout and business tracks.
