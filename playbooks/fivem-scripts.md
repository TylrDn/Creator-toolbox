# FiveM scripts playbook

## Opportunity thesis

RP servers buy maintained scripts with docs and support. One good job or economy resource can outperform dozens of free snippets if updates and compatibility are reliable.

## Who the buyer is

Server owners with 30-200 active players who outgrew free resources and need config-driven customization.

## What to build first

Start with **custom job system** (see `scripts/specs/job-system.md`). It touches economy, UI, and progression hooks other products can extend.

## Weekly shipping cadence

- Week 1: spec + config schema + empty resource skeleton
- Week 2: clock in/out + one sample job end-to-end
- Week 3: admin tools + logging
- Week 4: docs, demo video, catalog listing update

## KPIs

- Demo server uptime
- Support tickets per sale
- Refund/chargeback rate
- Repeat buyers on second product

## Common failure modes

- Supporting too many frameworks at once
- No exploit testing on payouts
- Shipping without install docs or load order

## Next actions

1. Run `python scripts/tools/generate_lua.py --out output/job-system-prompt.json`
2. Set status to `in_progress` in `scripts/catalog.yaml` when coding starts
3. Record a 60s devlog short for the content calendar
