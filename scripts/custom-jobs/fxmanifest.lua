fx_version 'cerulean'
game 'gta5'

name 'custom-jobs'
description 'Config-driven job framework (standalone v1)'
author 'Creator Toolbox'
version '1.0.0'

lua54 'yes'

shared_scripts {
    'shared/constants.lua',
    'shared/jobs.lua',
}

client_scripts {
    'client/main.lua',
}

server_scripts {
    'server/main.lua',
}
