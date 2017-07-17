#!/usr/bin/env python

import clsRest as r
import yaml
import imp, os
import re

EXT_PY   = 'py'
EXT_YAML = 'yaml'
EXT_NONE = 'none'
REG_PARSER_FILE = r'(.*)\.(.*)\[(.*)\]'

def importYaml(yamlName):
    with open(yamlName, 'r') as f: doc = yaml.safe_load(f.read())
    return doc

def createTs(tsDict):
    for tsId, tsTestCaseList in tsDict.iteritems():
        return r.TestSuite(tsId, tsTestCaseList)

def parserTsArgs(tsFile):
    tsFileName, tsModule, tsFileExt, tsArgs = tsFile, None, EXT_NONE, None
    m = re.search(REG_PARSER_FILE, tsFile)
    if m:
        tsFileName = m.group(1)+'.'+m.group(2)
        tsModule = m.group(1).replace('/', '.')
        tsFileExt = m.group(2)
        tsArgs = m.group(3)
    return tsFileName, tsModule, tsFileExt, tsArgs

def genTsFromFile(tsFile):
    tsFileName, tsModule, tsFileExt, tsArgs = parserTsArgs(tsFile)
    if tsFileExt == EXT_PY:
        print tsModule, tsFileName
        print os.getcwd()
        tsImportModule = imp.load_source(tsModule, tsFileName)
        return createTs(tsImportModule.generateTs(tsArgs))
    elif tsFileExt == EXT_YAML:
        return createTs(importYaml(tsFileName))
    else:
        return None