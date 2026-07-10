# RP server playbook

## Opportunity thesis

If platform rules allow, curated RP servers can earn recurring revenue from subscriptions and events. Clips and creator collabs drive applications more than ads alone.

## Who the buyer is

Players seeking structured RP with fair moderation and stable economy. Secondary audience: streamers looking for clip-friendly servers.

## What to build first

Core loop: apply → whitelist → starter job → first event. Document rules and economy before opening donations.

## Weekly shipping cadence

- Week 1: rules, Discord structure, application flow
- Week 2: economy tuning + 2 entry jobs
- Week 3: first public event + clip pipeline
- Week 4: subscription tier test (small group)

## KPIs

- Active players (peak concurrent)
- Application completion rate
- Subscriber count and churn
- Moderator response time

## Common failure modes

- Opening before moderation staffing
- Pay-to-win perks that kill RP quality
- No content pipeline (server feels empty online)

## Next actions

1. Run `python -m orchestrator rp_server_launch --var event_name="Launch night"`
2. Align `servers/design.md` with your faction list
3. Schedule launch posts in `content/calendar.yaml`
