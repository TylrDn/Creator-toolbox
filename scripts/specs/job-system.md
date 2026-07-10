# Custom job system (FiveM-compatible)

Product spec for a configurable job framework targeting RP server owners on FiveM/RedM-compatible stacks. Verify platform compatibility against current Rockstar and Cfx.re terms before shipping.

## Problem

Server owners need jobs that feel unique but cannot afford to rewrite boilerplate for every role. Copy-paste scripts lack documentation, config, and support.

## Solution

A job system with:

- Job definitions in YAML or JSON (role name, blip, uniform, vehicle spawn)
- Payout rules tied to server economy config
- Optional progression (ranks, unlocks) per job
- Admin commands to assign, debug, and reset jobs
- Exports/events for other resources (inventory, banking)

## Non-goals (v1)

- Full minigame suite for every job
- Paid marketplace integration (sell via your own site initially)
- Cross-server sync

## User stories

1. As an admin, I add a "delivery driver" job in config without editing core Lua.
2. As a player, I clock in, receive a uniform and vehicle, complete tasks, and get paid.
3. As a developer, I hook my inventory resource to job completion events.

## Technical outline

```
resources/
  custom-jobs/
    fxmanifest.lua
    config/jobs.yaml
    client/main.lua
    server/main.lua
    shared/constants.lua
```

- **Config loader**: parse jobs.yaml at resource start; validate required fields.
- **State machine**: off-duty → on-duty → task active → payout → cooldown.
- **Security**: server-side payout validation; rate limits on task completion.
- **Observability**: structured logs for admin audit (job start, payout, exploit flags).

## Config example (sketch)

```yaml
jobs:
  delivery_driver:
    label: Delivery Driver
    blip: { sprite: 477, color: 5 }
    payout: { base: 150, bonus_per_stop: 25 }
    vehicle: "boxville2"
    uniform: { component: 11, drawable: 15 }
```

## Testing plan

- Unit-style tests for config validation (Python helper or in-resource checks).
- Manual QA checklist: clock in/out, payout, exploit attempts (spam complete).
- Test on a clean server with only economy + inventory dependencies.

## Documentation deliverables

- Install guide (dependencies, load order)
- Config reference for every job field
- Event/export reference for integrators
- Migration notes from v1 to v2

## Pricing hypothesis

- Starter tier (3 jobs): lower price point
- Pro tier (unlimited jobs + progression): higher price with support window

## Open questions

- Which inventory/banking resources to support out of the box?
- ESX vs QBCore vs standalone: pick one for v1 or abstract behind adapters?

Use `scripts/tools/generate_lua.py` to turn this spec into an LLM prompt for implementation drafts.
