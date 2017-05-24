#!/usr/bin/env python

import clsRest as r

LABEL_TESTSUITE = 'EASYCURL_TESTSUITE'
EXT_PY = 'py'

def genTsFromFile(tsFile):
    tsFileExt = tsFile.split('.')[-1]
    tsFileName = '.'.join(tsFile.split('.')[:-1])
    if tsFileExt == EXT_PY:
        tsImportModule = __import__(tsFileName, globals(), locals(), [LABEL_TESTSUITE], -1)
        tsId, tsTestCaseList = tsImportModule.EASYCURL_TESTSUITE
        return r.TestSuite(tsId, tsTestCaseList)
    else:
        return None