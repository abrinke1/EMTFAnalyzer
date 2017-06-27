
# ## Basic (but usually unnecessary) imports
# import os
# import sys
# import commands

import subprocess

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('reL1T',eras.Run2_2016)

## Import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.GeometryRecoDB_cff') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.MagneticField_cff') ## Different than in data ("MagneticField_AutoFromDBCurrent_cff"?)
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff') ## Different than in data
process.load('Configuration.StandardSequences.RawToDigi_cff') ## Different than in data ("RawToDigi_Data_cff"?)
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi')

## CSCTF digis, phi / pT LUTs?
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")

## Import RECO muon configurations
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

## Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v14', '') ## Different than in data ("auto:run2_data"?)

# ## Event Setup Producer
# process.load('L1TriggerSep2016.L1TMuonEndCap.fakeEmtfParams_cff') ## Why does this file have "fake" in the name? - AWB 18.04.16
# process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
#                                 toGet = cms.VPSet(
#         ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/ (Important? - AWB 18.04.16)
#         cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
#                  data = cms.vstring('L1TMuonEndcapParams'))
#         ),
#                                 verbose = cms.untracked.bool(True)
#                                 )

readFiles = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles
    )

eos_cmd = '/afs/cern.ch/project/eos/installation/pro/bin/eos.select'

## in_dir_name = '/store/relval/CMSSW_8_0_19/RelValNuGun_UP15/GEN-SIM-DIGI-RECO/PU25ns_80X_mcRun2_asymptotic_2016_TrancheIV_v2_Tr4GT_v2_FastSim-v1/00000/'
in_dir_name = '/store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/'
# in_dir_name = '/store/user/abrinke1/EMTF/MC/JPsiToMuMu_Pt20to120_EtaPhiRestricted-pythia8-gun/'

out_dir_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/'

for in_file_name in subprocess.check_output([eos_cmd, 'ls', in_dir_name]).splitlines():
    if not ('.root' in in_file_name): continue
    readFiles.extend( cms.untracked.vstring(in_dir_name+in_file_name) )

# dir_str = 'root://cms-xrd-global.cern.ch/'
# dir_str += '/store/mc/RunIISpring16DR80/SingleMu_Pt1To1000_FlatRandomOneOverPt/GEN-SIM-RAW/NoPURAW_NZS_withHLT_80X_mcRun2_asymptotic_v14-v1/60000/'

# readFiles.extend([
        
        # ## Tau-to-3-mu MC
        # 'root://eoscms.cern.ch//eos/cms/store/user/wangjian/DsTau3Mu_FullSim_1007/merged_fltr.root'

        ## SingleMu MC, noPU, flat in 1/pT
        ## DAS: dataset=/SingleMu_Pt1To1000_FlatRandomOneOverPt/RunIISpring16DR80-NoPURAW_NZS_withHLT_80X_mcRun2_asymptotic_v14-v1/GEN-SIM-RAW

        # 'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/26CA310A-4164-E611-BE48-001E67248566.root',

        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/14C3C3CB-3864-E611-B770-20CF3027A624.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/401C4E92-3F64-E611-B190-00259090765E.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/4645B2E7-3864-E611-9724-5404A64A1265.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/507EEB74-3964-E611-B03B-3417EBE5361A.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/644DC20B-3464-E611-9858-0025909083EE.root',

        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/683F88CB-4464-E611-AE40-20CF3027A5D8.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/74715FCC-3864-E611-AA0F-3417EBE539DA.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/769D60D3-3964-E611-8D1C-44A8423D7989.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/A6DBC3A6-E964-E611-8798-002590907826.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/D24C4348-3664-E611-BFB7-00259090784E.root',

        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/E4541CA0-3664-E611-9DC1-00221982B650.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/E8BE669B-3C64-E611-9170-00259090766E.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/EEF06A5C-3564-E611-8F72-002590908EC2.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/F04B42E3-3D64-E611-AA23-0025909083EE.root',
        # 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/MC/SingleMu_Pt1To1000_FlatRandomOneOverPt/FCC1A3C5-4064-E611-8812-002590907836.root',

        # dir_str+'14C3C3CB-3864-E611-B770-20CF3027A624.root',
        # dir_str+'4645B2E7-3864-E611-9724-5404A64A1265.root',
        # dir_str+'507EEB74-3964-E611-B03B-3417EBE5361A.root',
        # dir_str+'683F88CB-4464-E611-AE40-20CF3027A5D8.root',
        # dir_str+'74715FCC-3864-E611-AA0F-3417EBE539DA.root',
        # dir_str+'769D60D3-3964-E611-8D1C-44A8423D7989.root',
        # dir_str+'E4541CA0-3664-E611-9DC1-00221982B650.root',

        # dir_str+'401C4E92-3F64-E611-B190-00259090765E.root',
        # dir_str+'644DC20B-3464-E611-9858-0025909083EE.root',
        # dir_str+'A6DBC3A6-E964-E611-8798-002590907826.root',
        # dir_str+'D24C4348-3664-E611-BFB7-00259090784E.root',
        # dir_str+'E8BE669B-3C64-E611-9170-00259090766E.root',
        # dir_str+'EEF06A5C-3564-E611-8F72-002590908EC2.root',
        # dir_str+'F04B42E3-3D64-E611-AA23-0025909083EE.root',
        # dir_str+'FCC1A3C5-4064-E611-8812-002590907836.root',

        # dir_str+'26CA310A-4164-E611-BE48-001E67248566.root',
        # dir_str+'2C138BAC-4164-E611-8D9C-001E6724865B.root',
        # dir_str+'4CF53555-4164-E611-8347-001E67248566.root',
        # dir_str+'7E409BA3-3D64-E611-B392-001E67248142.root',
        # dir_str+'AE863F4E-3764-E611-977A-001E67248A25.root',
        # dir_str+'E65524B4-E964-E611-805F-0CC47A7139C4.root',

        # ])

process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")


# Path and EndPath definitions

## Defined in Configuration/StandardSequences/python/SimL1EmulatorRepack_FullMC_cff.py
# process.L1RePack_step = cms.Path(process.SimL1Emulator)
SimL1Emulator_AWB = cms.Sequence(process.unpackRPC+process.unpackCSC)
process.L1RePack_step = cms.Path(SimL1Emulator_AWB)

## Defined in Configuration/StandardSequences/python/RawToDigi_cff.py
## Includes L1TRawToDigi, defined in L1Trigger/Configuration/python/L1TRawToDigi_cff.py
# process.raw2digi_step = cms.Path(process.RawToDigi)

process.simCscTriggerPrimitiveDigis.CSCComparatorDigiProducer = cms.InputTag('unpackCSC', 'MuonCSCComparatorDigi')
process.simCscTriggerPrimitiveDigis.CSCWireDigiProducer       = cms.InputTag('unpackCSC', 'MuonCSCWireDigi')

## process.load('L1TriggerSep2016.L1TMuonEndCap.simEmtfDigis_cfi')
process.load('L1TriggerSep2016.L1TMuonEndCap.simEmtfDigisSep2016_cfi')

process.simEmtfDigisSep2016.MinBX = cms.int32(-3)
process.simEmtfDigisSep2016.MaxBX = cms.int32(+3)

process.simEmtfDigisSep2016.spPCParams16.FixZonePhi     = cms.bool(True)
process.simEmtfDigisSep2016.spPCParams16.UseNewZones    = cms.bool(True)
#process.simEmtfDigisSep2016.spPCParams16.ZoneBoundaries = cms.vint32(0,41,49,87,127)
process.simEmtfDigisSep2016.spPCParams16.ZoneBoundaries = cms.vint32(0,36,54,96,127)

process.simEmtfDigisSep2016.spPRParams16.UseSymmetricalPatterns = cms.bool(True)

process.simEmtfDigisSep2016.spGCParams16.UseSecondEarliest = cms.bool(True)

process.simEmtfDigisSep2016.spPAParams16.FixMode15HighPt = cms.bool(True)
process.simEmtfDigisSep2016.spPAParams16.Bug9BitDPhi     = cms.bool(False)
process.simEmtfDigisSep2016.spPAParams16.BugMode7CLCT    = cms.bool(False)
process.simEmtfDigisSep2016.spPAParams16.BugNegPt        = cms.bool(False)

process.simEmtfDigisSep2016.CSCInput        = cms.InputTag('simCscTriggerPrimitiveDigis','MPCSORTED')
process.simEmtfDigisSep2016.RPCInput        = cms.InputTag('simMuonRPCDigis')
process.simEmtfDigisSep2016.CSCEnable       = cms.bool(True)
process.simEmtfDigisSep2016.RPCEnable       = cms.bool(True)
process.simEmtfDigisSep2016.CSCInputBXShift = cms.int32(-6)
process.simEmtfDigisSep2016.RPCInputBXShift = cms.int32(0)
process.simEmtfDigisSep2016.verbosity       = cms.untracked.int32(0)

## NTuplizer
process.ntuple = cms.EDAnalyzer('PtLutInput',
                                isMC          = cms.bool(True),
                                genMuonTag    = cms.InputTag("genParticles"),    ## GEN muons
                                emtfHitTag    = cms.InputTag("simEmtfDigisSep2016"),  ## EMTF input LCTs
                                emtfTrackTag  = cms.InputTag("simEmtfDigisSep2016"),  ## EMTF emulator output tracks
                                )


RawToDigi_AWB = cms.Sequence(process.simCscTriggerPrimitiveDigis+process.muonCSCDigis+process.muonRPCDigis+process.csctfDigis+process.simEmtfDigisSep2016+process.ntuple)
process.raw2digi_step = cms.Path(RawToDigi_AWB)

## Defined in Configuration/StandardSequences/python/EndOfProcess_cff.py
process.endjob_step = cms.EndPath(process.endOfProcess)

# process.L1TMuonSeq = cms.Sequence(
#     process.muonCSCDigis + ## Unpacked CSC LCTs from TMB
#     process.csctfDigis + ## Necessary for legacy studies, or if you use csctfDigis as input
#     process.muonRPCDigis +
#     ## process.esProd + ## What do we loose by not having this? - AWB 18.04.16
#     process.emtfStage2Digis +
#     process.simEmtfDigisSep2016
#     ## process.ntuple
#     )

# process.L1TMuonPath = cms.Path(
#     process.L1TMuonSeq
#     )


## NTuple output File
process.TFileService = cms.Service(
    "TFileService",
    # fileName = cms.string("EMTF_MC_NTuple_Tau3Mu.root")
    # fileName = cms.string(out_dir_name+'EMTF_MC_NTuple_SingleMu_noRPC_300k.root')
    fileName = cms.string('EMTF_MC_NTuple_SingleMu_RPC_test.root')
    # fileName = cms.string('EMTF_MC_NTuple_JPsi_noRPC_50k.root')
    )


# outCommands = cms.untracked.vstring('keep *')
outCommands = cms.untracked.vstring(

    'keep recoMuons_muons__*',
    'keep *Gen*_*_*_*',
    'keep *_*Gen*_*_*',
    'keep *gen*_*_*_*',
    'keep *_*gen*_*_*',
    'keep CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_*_*_*', ## muonCSCDigis
    'keep RPCDetIdRPCDigiMuonDigiCollection_*_*_*', ## muonRPCDigis
    #'keep CSCCorrelatedLCTDigiCollection_muonCSCDigis_*_*',
    #'keep *_*_*muonCSCDigis*_*',
    #'keep *_*_*_*muonCSCDigis*',
    'keep *_csctfDigis_*_*',
    'keep *_emtfStage2Digis_*_*',
    'keep *_simEmtfDigis_*_*',
    'keep *_simEmtfDigisSep2016_*_*',
    'keep *_simEmtfDigisSep2016MC_*_*',
    'keep *_gmtStage2Digis_*_*',
    'keep *_simGmtStage2Digis_*_*',

    )

# process.treeOut = cms.OutputModule("PoolOutputModule", 
#                                    # fileName = cms.untracked.string("EMTF_MC_Tree_RelValNuGun_UP15_1k.root"),
#                                    # fileName = cms.untracked.string("EMTF_MC_Tree_tau_to_3_mu_RPC_debug.root"),
#                                    fileName = cms.untracked.string(out_dir_name+'EMTF_MC_Tree_SingleMu_noRPC_300k.root'),
#                                    outputCommands = outCommands
#                                    )

# process.treeOut_step = cms.EndPath(process.treeOut) ## Keep output tree - AWB 08.07.16

# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step,process.raw2digi_step,process.endjob_step)
# process.schedule = cms.Schedule(process.L1RePack_step,process.raw2digi_step,process.endjob_step,process.treeOut_step)

# process.output_step = cms.EndPath(process.treeOut)
# process.schedule = cms.Schedule(process.L1TMuonPath)
# process.schedule.extend([process.output_step])

# ## What does this do? Necessary? - AWB 29.04.16
# from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
# process = customise_csc_PostLS1(process)
