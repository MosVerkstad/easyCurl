#!/usr/bin/env python

import clsRest as r
import yaml

LABEL_TESTSUITE = 'EASYCURL_TESTSUITE'
EXT_PY   = 'py'
EXT_YAML = 'yaml'

def importYaml(yamlName):
    with open(yamlName, 'r') as f: doc = yaml.safe_load(f.read())
    return doc

def createTs(tsDict):
    for tsId, tsTestCaseList in tsDict.iteritems():
        return r.TestSuite(tsId, tsTestCaseList)

def genTsFromFile(tsFile):
    tsFileExt = tsFile.split('.')[-1]
    tsFileName = '.'.join(tsFile.split('.')[:-1])
    if tsFileExt == EXT_PY:
        tsImportModule = __import__(tsFileName, globals(), locals(), [LABEL_TESTSUITE], -1)
        return createTs(tsImportModule.EASYCURL_TESTSUITE)
    elif tsFileExt == EXT_YAML:
        return createTs(importYaml(tsFile))
    else:
        return None