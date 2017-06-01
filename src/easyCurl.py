#!/usr/bin/python

import pycurl
from datetime import datetime
import time
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from easyCurlConfig import optCurlMethods, optCurlLogName

CONTROL_OPT_LOOP = 'LOOP'
CONTROL_OPT_DELAY = 'DELAY'

def setOptCurl(c, opts):
    for opt in opts:
        if opt[1] == 'int':    c.setopt(eval(opt[0]), int(eval(opt[2])))
        elif opt[1] == 'bool': c.setopt(eval(opt[0]), bool(eval(opt[2])))
        elif opt[1] == 'raw':  c.setopt(eval(opt[0]), opt[2])
    return c

def runCurl(requestObj):
    url, method, requestHeaders, requestBodyStr = requestObj
    requestBody = BytesIO(requestBodyStr)
    responseHeaders = BytesIO()
    responseBody = BytesIO()
    responseCode, responseHeaderStr, responseBodyStr = None, None, None

    c = setOptCurl(setOptCurl(pycurl.Curl(), optCurlMethods['COMMON']), optCurlMethods[method])

    c.setopt(c.URL, url)
    c.setopt(c.HTTPHEADER, requestHeaders)
    c.setopt(c.READFUNCTION, requestBody.read)
    c.setopt(c.HEADERFUNCTION, responseHeaders.write)
    c.setopt(c.WRITEFUNCTION, responseBody.write)

    try:
        startTime = datetime.now()
        c.perform()
        endTime = datetime.now()
    except Exception as e:
        responseCode, responseHeaderStr, responseBodyStr, startTime, endTime = None, None, None, None, None
    else:
        responseCode, responseHeaderStr, responseBodyStr = c.getinfo(pycurl.RESPONSE_CODE), responseHeaders.getvalue(), responseBody.getvalue()
    finally:
        c.close()
        requestBody.close()
        responseHeaders.close()
        responseBody.close()

    return responseCode, responseHeaderStr, responseBodyStr, startTime, endTime

from easyCurlTest import genTsFromFile 
from clsRest import *
import sys, getopt
import uuid

def parserOptions():
    optionsLong = ['help', 'suite', 'display', 'report']
    optionsShort = 'hs:d:r:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], optionsShort, optionsLong)
    except getopt.GetoptError:
        showHelp()

    if len(opts) <= 0: showHelp()

    suite = None
    display = None
    report = None
    for o, a in opts:
        if o in ('-h', '--help'): showHelp()
        if o in ('-s', '--suite'): suite = a
        if o in ('-d', '--display'): display = a
        if o in ('-r', '--report'): report = a

    return suite, display if display != None else 'progress', report

def showHelp():
    helpMsg = 'Designed by Shirley Mosverkstad\n'\
        'Usage: easyCurl [OPTION]...\n\n'\
        '    -h, --help        Show this help\n'\
        '    -s, --suite       Provide the test suite file name '\
        'so far the supported file type: py, yaml, json, xml\n'\
        '    -d, --display     [default: progress] Provide the test '\
        'display in the screen, value: progress or verbose.\n'\
        '    -r, --report      (ongoing).\n\n'
    sys.stdout.write(helpMsg)
    sys.exit(3)

def totalRc(testSuite):
    total = 0
    for cnt in range(int(testSuite.getControl().getOpt(CONTROL_OPT_LOOP))):
        for testCase in testSuite.getTestCases():
            for cnt in range(int(testCase.getControl().getOpt(CONTROL_OPT_LOOP))):
                for restCase in testCase.getRestCases():
                    total = total + 1
    return total

def printProgress(current, total):
    progress = str(current * 1.0 / total * 100)
    progressLeft, progressRight = progress.split('.')[0], progress.split('.')[1]
    progressLeft = ' '*(3 - len(progressLeft)) + progressLeft if len(progressLeft) < 3 else progressLeft
    progressRight = progressRight + '0'*(2 - len(progressRight)) if len(progressRight) < 2 else progressRight[:2]
    progress = progressLeft + '.' + progressRight + '%'
    completeNum = int(current * 1.0 / total * 50)
    uncompleteNum = 50 - completeNum
    bar = '[' + '='*completeNum + ' '*uncompleteNum + ']'
    status = bar + progress + ' (' + str(current) + '/' + str(total) + ')'
    sys.stdout.write('\r' + status)
    sys.stdout.flush()

def verbose(display): return display == 'verbose'

def genPId(): return str(uuid.uuid4().hex)[:8]

if(__name__ == '__main__'):
    suite, display, report = parserOptions()
    testSuite = genTsFromFile(suite)

    fLog = open(optCurlLogName, 'w')
    total = totalRc(testSuite)
    current = 0
    for cnt in range(int(testSuite.getControl().getOpt(CONTROL_OPT_LOOP))):
        testSuite.setPId(genPId())

        for testCase in testSuite.getTestCases():
             for cnt in range(int(testCase.getControl().getOpt(CONTROL_OPT_LOOP))):
                 testCase.setPId(genPId())

                 for restCase in testCase.getRestCases():
                     restCase.setPId(genPId())
                     requestBodyStr = restCase.getRequest().getBody()
                     restCase.setResponse(Response(runCurl(restCase.getRequest().getProperty())))
                     restCase.getRequest().setStartTime(restCase.getResponse().getStartTime())

                     current = current + 1
                     if not verbose(display): printProgress(current, total)

                 if verbose(display): print testCase
                 fLog.write(str(testCase) + '\n\n')
                 testCase.clean()
                 time.sleep(int(testCase.getControl().getOpt(CONTROL_OPT_DELAY)))

        time.sleep(int(testSuite.getControl().getOpt(CONTROL_OPT_DELAY)))

    fLog.close()
    print