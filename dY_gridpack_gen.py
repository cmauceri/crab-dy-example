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
[cmauceri@lxplus932 CrabTest]$ cat dy_gridpack.py 
import os
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

process = cms.Process('GEN')

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10))

seed = int(os.environ.get("JOB_SEED", "12345"))
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(seed)
process.RandomNumberGeneratorService.externalLHEProducer = cms.PSet(
    initialSeed = cms.untracked.uint32(seed + 1),
    engineName = cms.untracked.string('HepJamesRandom'),
)

process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/slc7_amd64_gcc700/Madgraph5_2.6.5/DY01234j_LO_5f_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(50),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(False),
)

process.generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 19.',
            'JetMatching:nQmatch = 5',
            'JetMatching:nJetMax = 4',
            'JetMatching:doShowerKt = off',
            'TimeShower:mMaxGamma = 4.0',
            'BeamRemnants:primordialKThard = 2.48',
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8PSweightsSettings',
            'processParameters',
        ),
    ),
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('dy_out.root'))

process.p = cms.Path(process.externalLHEProducer * process.generator)
process.outpath = cms.EndPath(process.out)
