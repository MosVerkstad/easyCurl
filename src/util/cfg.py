#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from vdy import vdy
from erc import erc
import re

REG_FILE_EXT = '(.*)\.(.*)'

SEPERATE_COMMA = ','
EXT_YAML = 'yaml'
EXT_YML  = 'yml'
EXT_VDY  = 'vdy'
EXT_ERC  = 'erc'
EXT_NONE = 'none'

def getExt(fileName):
    m = re.search(REG_FILE_EXT, fileName)
    if m: return m.group(2)
    else: return EXT_NONE

def isYaml(fileName):
    return True if getExt(fileName)==EXT_YAML or getExt(fileName)==EXT_YML else False

def isVdy(fileName):
    return True if getExt(fileName)==EXT_VDY else False

def isErc(fileName):
    return True if getExt(fileName)==EXT_ERC else False

def importYaml(yamlName):
    with open(yamlName, 'r') as f: doc = yaml.safe_load(f.read())
    return doc

def importYamlList(yamlNameList):
    doc = dict()
    for y in yamlNameList:
        doc.update(importYaml(y))
    return doc

def getArgv(argvString): return argvString.split(SEPERATE_COMMA)

def getYamlConfig(fileList):
    doc = dict()
    for f in fileList:
        if isYaml(f):
            doc.update(importYaml(f))
    return doc

def getErcConfig(fileList):
    vdyList = list()
    ercList = list()
    for f in fileList:
        if isVdy(f) or isYaml(f): vdyList.append(f)
        elif isErc(f): ercList.append(f)
    common = vdy(vdyList)
    return erc(vdy(vdyList), importYamlList(ercList))