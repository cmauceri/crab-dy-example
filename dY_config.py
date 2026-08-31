from CRABClient.UserUtilities import config
config = config()

config.General.requestName   = 'DY_gridpack_privateMC'
config.General.workArea      = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'dy_gridpack.py'
config.JobType.numCores    = 1
config.JobType.maxMemoryMB = 3000
config.JobType.maxJobRuntimeMin = 240

config.Data.outputPrimaryDataset = 'DYJetsToLL_privateMC'
config.Data.splitting     = 'EventBased'
config.Data.unitsPerJob   = 10      # events per job
config.Data.totalUnits    = 10      # total events
config.Data.publication   = False
config.Data.outputDatasetTag = 'DY_gridpack_test'
config.Data.outLFNDirBase = '/store/user/cmauceri/crab-test'

config.Site.storageSite = 'T3_US_Brown'
