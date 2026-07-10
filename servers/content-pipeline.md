# Server content pipeline

How the RP server generates acquisition through clips, shorts, Discord, and email.

## Goals

- Fill whitelist applications with qualified players
- Produce weekly clip fuel for YouTube/TikTok
- Retain subscribers through event cadence and transparency

## Channels

| Channel | Purpose | Owner |
|---------|---------|-------|
| YouTube long-form | Server tours, rule explainers, patch notes | Content lead |
| Shorts/TikTok | Clip highlights, funny moments, POV hooks | Clippers + editors |
| Discord | Applications, announcements, LFG | Community mod |
| Email | Monthly recap, event calendar, policy updates | Ops |

## Weekly rhythm

1. **Monday**: post patch notes or admin blog in Discord + email snippet
2. **Wednesday**: release 2-3 shorts from prior week's best clips
3. **Friday**: scheduled in-server event (race, market, community court)
4. **Sunday**: clip contest submission deadline; winners featured Monday

## Clip sourcing

- Encourage streamers to opt in to a `#clips` channel
- Moderators tag clips with consent and player handles
- IP-safe only: no leaked assets; use in-game capture or approved overlays

## Shorts workflow

Use orchestrator workflow `rp_server_launch` or manual templates:

- Hook: one sentence outcome ("We rebuilt the economy in 30 days")
- Body: 2-3 fast cuts with on-screen text
- CTA: Discord apply link

## Email workflow

- Subject: one event or change
- Body: 3 bullets max + single CTA
- Template: `templates/content/email-update.md`

## Metrics

- Applications per week
- Clip submissions vs shorts published
- Discord joins from short-link UTM tags
- Event attendance (peak concurrent players)

## Integration with Creator Toolbox

- `content/calendar.yaml` schedules server-themed posts
- `orchestrator/workflows/rp_server_launch.yaml` drafts Discord + short assets
- `orchestrator/workflows/community_onboarding.yaml` drafts onboarding posts
- `config/games/gta6.yaml` supplies game name and channel names
