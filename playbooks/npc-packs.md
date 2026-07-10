# NPC packs playbook

## Opportunity thesis

Ambient NPCs improve server feel. Packaged configs plus a prompt engine let owners add characters without hiring writers for every line.

## Who the buyer is

Mid-size RP servers (50+ active) that want bar/shop/quest NPCs with consistent voice and safety boundaries.

## What to build first

Ship the **bartender** example (`npc-packs/config/bartender.yaml`) with engine docs and a 2-minute demo video.

## Weekly shipping cadence

- Week 1: engine + bartender config + safety boundaries
- Week 2: shopkeeper config + integration notes
- Week 3: sales page draft via `npc_pack_release` workflow
- Week 4: beta on one partner server, collect latency metrics

## KPIs

- Prompt latency (p50/p95)
- Cost per 1k NPC lines (when using paid inference)
- Beta server retention feedback
- Pack sales or license inquiries

## Common failure modes

- Unbounded token usage
- NPCs coaching rule breaks or toxic speech
- No versioning when configs change

## Next actions

1. `python npc-packs/engine.py` to inspect sample prompt JSON
2. Add quest giver YAML following bartender pattern
3. Run `python -m orchestrator npc_pack_release --var summary="Bartender pack beta"`
