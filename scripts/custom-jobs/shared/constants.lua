-- Job state constants
JobState = {
    OFF_DUTY = 'off_duty',
    ON_DUTY = 'on_duty',
    TASK_ACTIVE = 'task_active',
    COOLDOWN = 'cooldown',
}

-- Default limits (override in server.cfg if needed)
Config = {
    PayoutCooldownMs = 5000,
    MaxTasksPerMinute = 6,
    AdminAce = 'customjobs.admin',
}

Events = {
    CLOCK_IN = 'customjobs:clockIn',
    CLOCK_OUT = 'customjobs:clockOut',
    COMPLETE_TASK = 'customjobs:completeTask',
    PAYOUT = 'customjobs:payout',
}

Exports = {
    GetPlayerJob = 'GetPlayerJob',
    IsOnDuty = 'IsOnDuty',
}
