# AI NPC pack product

Packaged NPC configs that turn role + player history + scene context into dialogue prompts for RP servers.

## What it does

- Loads YAML per NPC (role, personality, safety boundaries)
- Builds system/user prompt pairs via `npc-packs/engine.py`
- Stays local-first: no API calls in the default path

## Target customer

RP server owners who want ambient NPCs (bartenders, shopkeepers, quest givers) without scripting every line by hand.

## Pricing approaches (hypothesis)

- Per-NPC license for small servers
- Bundle pricing (10 NPCs) for mid-size communities
- Annual support tier for config updates and new roles

## Deployment considerations

- Run inference on your own infrastructure or a provider you trust
- Cache frequent greetings to cut latency and cost
- Version configs; servers pin a pack version for reproducibility

## Latency and cost constraints

- Target sub-2s turn time for bar/chit-chat NPCs
- Cap tokens per reply; bartender config suggests ~120 tokens
- Batch non-urgent NPC lines (radio ads, ambient chatter) offline

## Safety constraints

- Boundaries list in each NPC YAML (no rule-breaking coaching, no sexual content, etc.)
- Log prompts and outputs for moderation review during beta
- Align with server rules and platform terms on AI-generated dialogue

## Next steps

1. Add 2-3 more example configs (shopkeeper, quest giver)
2. Wire `npc_pack_release` workflow to sales email template
3. Document integration pattern for FiveM resource (future)
