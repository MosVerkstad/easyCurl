#!/usr/bin/env python

import clsRest as r
import yaml

EXT_PY   = 'py'
EXT_YAML = 'yaml'
BRAKET_LEFT = '['
BRAKET_RIGHT = ']'

def importYaml(yamlName):
    with open(yamlName, 'r') as f: doc = yaml.safe_load(f.read())
    return doc

def createTs(tsDict):
    for tsId, tsTestCaseList in tsDict.iteritems():
        return r.TestSuite(tsId, tsTestCaseList)

def parserTsArgs(tsFile):
    tsArgs = None
    tsFileName = tsFile
    posLeft = tsFile.find(BRAKET_LEFT)
    posRight = tsFile.find(BRAKET_RIGHT)
    if posLeft >= 0 and posRight >= 0:
        tsArgs = tsFile[posLeft+1 : posRight]
        tsFileName = tsFile[:posLeft]
    tsFileExt = tsFileName.split('.')[-1]
    tsFilePrefix = '.'.join(tsFileName.split('.')[:-1])
    return tsFileName, tsFilePrefix, tsFileExt, tsArgs

def genTsFromFile(tsFile):
    tsFileName, tsFilePrefix, tsFileExt, tsArgs = parserTsArgs(tsFile)
    if tsFileExt == EXT_PY:
        tsImportModule = __import__(tsFilePrefix, globals(), locals(), [], -1)
        return createTs(tsImportModule.generateTs(tsArgs))
    elif tsFileExt == EXT_YAML:
        return createTs(importYaml(tsFileName))
    else:
        return None
