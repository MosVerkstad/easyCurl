#!/usr/bin/python

from datetime import datetime
import time

from kernel.easyCurlConfig import optCurlMethods, optCurlLogName
from kernel.easyCurlKernel import runCurl

from wrap.easyCurlTest import genTsFromFile 
from wrap.clsRest import *
from wrap.clsSum import *
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
    tsSum = Sum()

    for cnt in range(int(testSuite.getControl().getOpt(CONTROL_OPT_LOOP))):
        tsPId = genPId()
        testSuite.setPId(tsPId)
        tsSum.addTs(tsPId, testSuite.getId())

        for testCase in testSuite.getTestCases():
             for cnt in range(int(testCase.getControl().getOpt(CONTROL_OPT_LOOP))):
                 tcPId = genPId()
                 testCase.setPId(tcPId)
                 tsSum.getTs(tsPId).addTc(tcPId, testCase.getId())

                 for restCase in testCase.getRestCases():
                     rcPId = genPId()
                     restCase.setPId(rcPId)

                     restCase.setResponse(Response(runCurl(restCase.getRequest().getProperty())))
                     restCase.getRequest().setStartTime(restCase.getResponse().getStartTime())

                     tsSum.getTs(tsPId).getTc(tcPId).addRc(rcPId, restCase.getMethod(), restCase.getUrl(), restCase.checkResult())

                     current = current + 1
                     if not verbose(display): printProgress(current, total)

                 if verbose(display): print testCase
                 fLog.write(str(testCase) + '\n\n')
                 testCase.clean()
                 time.sleep(int(testCase.getControl().getOpt(CONTROL_OPT_DELAY)))

        time.sleep(int(testSuite.getControl().getOpt(CONTROL_OPT_DELAY)))

    fLog.close()
    print
    print tsSum
