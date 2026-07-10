# Custom Jobs (FiveM standalone v1)

Config-driven job framework for RP servers. **Standalone v1** — no ESX/QBCore dependency. Hook payouts via the `customjobs:payout` server event.

## Install

1. Copy `scripts/custom-jobs/` into your server `resources/` folder as `custom-jobs`.
2. Add to `server.cfg`:
   ```
   ensure custom-jobs
   add_ace group.admin customjobs.admin allow
   ```
3. Adjust job locations in `shared/jobs.lua` (and mirror in `config/jobs.yaml` for docs).

## Player flow

1. Go to job blip / clock-in point.
2. Press **E** to clock in.
3. Press **E** at the same zone to complete delivery stops (3 stops = payout).
4. `/jobclockout` to end shift.

## Admin commands

| Command | Description |
|---------|-------------|
| `jobadmin_assign <id> <jobId>` | Force-assign a player to a job |
| `jobadmin_reset <id>` | Reset player job state |

Requires ace `customjobs.admin`.

## Config

Edit `shared/jobs.lua` to add jobs. Required fields per job:

- `label` — display name
- `clockIn` — `{ x, y, z, radius }`
- `payout` — `{ base, bonusPerStop }`
- `blip` — optional map blip settings

## Security

- Payouts validated server-side only.
- Rate limit: `Config.MaxTasksPerMinute` (default 6).
- Cooldown between payouts: `Config.PayoutCooldownMs` (default 5000 ms).
- Audit log printed to server console.

## Integrations

Listen for server event `customjobs:payout` to credit your economy:

```lua
AddEventHandler('customjobs:payout', function(playerId, amount, reason)
    -- Credit your banking resource here
end)
```

## Exports

- `exports['custom-jobs']:GetPlayerJob()` (client/server)
- `exports['custom-jobs']:IsOnDuty()` (client/server)

## Status

Beta — delivery driver job only. Test on a demo server before production.
