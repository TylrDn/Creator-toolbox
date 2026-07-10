-- Job definitions (mirrors config/jobs.yaml schema; Lua table for standalone v1)
Jobs = {
    delivery_driver = {
        label = 'Delivery Driver',
        blip = { sprite = 477, color = 5, scale = 0.8 },
        clockIn = { x = 127.5, y = -1284.0, z = 29.3, radius = 2.5 },
        payout = { base = 150, bonusPerStop = 25 },
        vehicle = 'boxville2',
        uniform = { component = 11, drawable = 15, texture = 0 },
        maxStopsPerTask = 3,
    },
}

function GetJob(jobId)
    return Jobs[jobId]
end

function ValidateJobs()
    for id, job in pairs(Jobs) do
        assert(job.label, ('job %s missing label'):format(id))
        assert(job.payout and job.payout.base, ('job %s missing payout.base'):format(id))
        assert(job.clockIn, ('job %s missing clockIn coords'):format(id))
    end
end
