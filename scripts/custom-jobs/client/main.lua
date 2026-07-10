local playerState = {
    jobId = nil,
    state = JobState.OFF_DUTY,
    stopsCompleted = 0,
}

local function notify(msg)
    BeginTextCommandThefeedPost('STRING')
    AddTextComponentSubstringPlayerName(msg)
    EndTextCommandThefeedPostTicker(false, true)
end

local function spawnJobBlips()
    for jobId, job in pairs(Jobs) do
        if job.blip and job.clockIn then
            local blip = AddBlipForCoord(job.clockIn.x, job.clockIn.y, job.clockIn.z)
            SetBlipSprite(blip, job.blip.sprite or 477)
            SetBlipColour(blip, job.blip.color or 5)
            SetBlipScale(blip, job.blip.scale or 0.8)
            SetBlipAsShortRange(blip, true)
            BeginTextCommandSetBlipName('STRING')
            AddTextComponentSubstringPlayerName(job.label)
            EndTextCommandSetBlipName(blip)
        end
    end
end

CreateThread(function()
    ValidateJobs()
    spawnJobBlips()
end)

CreateThread(function()
    while true do
        local sleep = 1000
        local ped = PlayerPedId()
        local coords = GetEntityCoords(ped)

        for jobId, job in pairs(Jobs) do
            local c = job.clockIn
            if c then
                local dist = #(coords - vector3(c.x, c.y, c.z))
                if dist < (c.radius or 2.5) then
                    sleep = 0
                    if playerState.state == JobState.OFF_DUTY then
                        BeginTextCommandDisplayHelp('STRING')
                        AddTextComponentSubstringPlayerName(('Press ~INPUT_CONTEXT~ to clock in as %s'):format(job.label))
                        EndTextCommandDisplayHelp(0, false, true, -1)
                        if IsControlJustReleased(0, 38) then
                            TriggerServerEvent(Events.CLOCK_IN, jobId)
                        end
                    elseif playerState.jobId == jobId and playerState.state == JobState.ON_DUTY then
                        BeginTextCommandDisplayHelp('STRING')
                        AddTextComponentSubstringPlayerName('Press ~INPUT_CONTEXT~ to complete delivery stop')
                        EndTextCommandDisplayHelp(0, false, true, -1)
                        if IsControlJustReleased(0, 38) then
                            TriggerServerEvent(Events.COMPLETE_TASK, jobId)
                        end
                    end
                end
            end
        end
        Wait(sleep)
    end
end)

RegisterNetEvent(Events.CLOCK_IN, function(jobId, newState)
    playerState.jobId = jobId
    playerState.state = newState
    playerState.stopsCompleted = 0
    local job = GetJob(jobId)
    notify(('Clocked in: %s'):format(job and job.label or jobId))
end)

RegisterNetEvent(Events.CLOCK_OUT, function()
    playerState.jobId = nil
    playerState.state = JobState.OFF_DUTY
    playerState.stopsCompleted = 0
    notify('Clocked out.')
end)

RegisterNetEvent(Events.PAYOUT, function(amount, reason)
    notify(('Paid $%s (%s)'):format(amount, reason or 'job'))
end)

RegisterCommand('jobclockout', function()
    TriggerServerEvent(Events.CLOCK_OUT)
end, false)

exports(Exports.IsOnDuty, function()
    return playerState.state ~= JobState.OFF_DUTY
end)

exports(Exports.GetPlayerJob, function()
    return playerState.jobId
end)
