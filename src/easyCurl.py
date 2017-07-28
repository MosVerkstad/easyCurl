#!/usr/bin/python

from kernel.easyCurlConfig import optCurlLogName
from kernel.easyCurlKernel import runCurl
from wrap.easyCurlTest import genTsFromFile
from wrap.clsRun import Run

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

if(__name__ == '__main__'):
    suite, display, report = parserOptions()
    testSuite = genTsFromFile(suite)

    tsRun = Run(runCurl, testSuite, optCurlLogName, display)
    tsRun.run()
