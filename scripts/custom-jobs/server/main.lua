local players = {}
local auditLog = {}

local function logAudit(src, action, detail)
    local entry = {
        time = os.time(),
        source = src,
        action = action,
        detail = detail or '',
    }
    auditLog[#auditLog + 1] = entry
    print(('[custom-jobs] %s player=%s %s'):format(entry.time, src, action))
end

local function getPlayerState(src)
    if not players[src] then
        players[src] = {
            jobId = nil,
            state = JobState.OFF_DUTY,
            stopsCompleted = 0,
            lastPayout = 0,
            taskTimestamps = {},
        }
    end
    return players[src]
end

local function rateLimitOk(state)
    local now = GetGameTimer()
    local window = 60000
    local cutoff = now - window
    local recent = {}
    for _, ts in ipairs(state.taskTimestamps) do
        if ts >= cutoff then
            recent[#recent + 1] = ts
        end
    end
    state.taskTimestamps = recent
    return #recent < Config.MaxTasksPerMinute
end

local function payPlayer(src, amount, reason)
    local state = getPlayerState(src)
    local now = GetGameTimer()
    if now - state.lastPayout < Config.PayoutCooldownMs then
        logAudit(src, 'payout_blocked', 'cooldown')
        return false
    end
    state.lastPayout = now
    -- Standalone v1: trigger client notification; hook banking export in integration layer
    TriggerClientEvent(Events.PAYOUT, src, amount, reason)
    logAudit(src, 'payout', ('amount=%s reason=%s'):format(amount, reason))
    TriggerEvent(Events.PAYOUT, src, amount, reason)
    return true
end

RegisterNetEvent(Events.CLOCK_IN, function(jobId)
    local src = source
    local job = GetJob(jobId)
    if not job then
        logAudit(src, 'clock_in_rejected', 'unknown_job')
        return
    end
    local state = getPlayerState(src)
    if state.state ~= JobState.OFF_DUTY then
        logAudit(src, 'clock_in_rejected', 'already_on_duty')
        return
    end
    state.jobId = jobId
    state.state = JobState.ON_DUTY
    state.stopsCompleted = 0
    logAudit(src, 'clock_in', jobId)
    TriggerClientEvent(Events.CLOCK_IN, src, jobId, JobState.ON_DUTY)
end)

RegisterNetEvent(Events.CLOCK_OUT, function()
    local src = source
    local state = getPlayerState(src)
    state.jobId = nil
    state.state = JobState.OFF_DUTY
    state.stopsCompleted = 0
    logAudit(src, 'clock_out', '')
    TriggerClientEvent(Events.CLOCK_OUT, src)
end)

RegisterNetEvent(Events.COMPLETE_TASK, function(jobId)
    local src = source
    local state = getPlayerState(src)
    local job = GetJob(jobId)

    if not job or state.jobId ~= jobId or state.state ~= JobState.ON_DUTY then
        logAudit(src, 'task_rejected', 'invalid_state')
        return
    end
    if not rateLimitOk(state) then
        logAudit(src, 'task_rejected', 'rate_limit')
        return
    end

    state.taskTimestamps[#state.taskTimestamps + 1] = GetGameTimer()
    state.stopsCompleted = state.stopsCompleted + 1

    local maxStops = job.maxStopsPerTask or 3
    local payout = job.payout.base + (job.payout.bonusPerStop or 0) * state.stopsCompleted

    if state.stopsCompleted >= maxStops then
        payPlayer(src, payout, jobId)
        state.state = JobState.COOLDOWN
        state.stopsCompleted = 0
        logAudit(src, 'task_complete', jobId)
        SetTimeout(Config.PayoutCooldownMs, function()
            if getPlayerState(src).jobId == jobId then
                getPlayerState(src).state = JobState.ON_DUTY
            end
        end)
    else
        logAudit(src, 'task_progress', ('stop=%s'):format(state.stopsCompleted))
    end
end)

RegisterCommand('jobadmin_reset', function(src, args)
    if src ~= 0 and not IsPlayerAceAllowed(src, Config.AdminAce) then
        return
    end
    local target = tonumber(args[1])
    if not target then
        return
    end
    players[target] = nil
    logAudit(src, 'admin_reset', ('target=%s'):format(target))
end, true)

RegisterCommand('jobadmin_assign', function(src, args)
    if src ~= 0 and not IsPlayerAceAllowed(src, Config.AdminAce) then
        return
    end
    local target = tonumber(args[1])
    local jobId = args[2]
    if not target or not GetJob(jobId) then
        return
    end
    local state = getPlayerState(target)
    state.jobId = jobId
    state.state = JobState.ON_DUTY
    TriggerClientEvent(Events.CLOCK_IN, target, jobId, JobState.ON_DUTY)
    logAudit(src, 'admin_assign', ('target=%s job=%s'):format(target, jobId))
end, true)

AddEventHandler('playerDropped', function()
    players[source] = nil
end)

exports(Exports.GetPlayerJob, function(src)
    return getPlayerState(src).jobId
end)

exports(Exports.IsOnDuty, function(src)
    return getPlayerState(src).state ~= JobState.OFF_DUTY
end)
