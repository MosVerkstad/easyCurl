#!/usr/bin/env python

import uuid
from datetime import datetime
import time

from clsRest import TestSuite, Response
from clsSum  import Sum
from clsShow import Show
from constants import *

class Run:
    def __init__(self, runFunc, testSuite, logName, display):
        self.runFunc = runFunc
        self.testSuite = testSuite
        self.tsSum = Sum()
        self.logName = logName
        self.tsLog = None
        self.tsShow = Show(display, self.totalRc())

    def totalRc(self):
        total = 0
        for cnt in range(int(self.testSuite.getControl().getOpt(CONTROL_OPT_LOOP))):
            for testCase in self.testSuite.getTestCases():
                for cnt in range(int(testCase.getControl().getOpt(CONTROL_OPT_LOOP))):
                    for restCase in testCase.getRestCases():
                        total += 1
        return total

    def genPId(self): return str(uuid.uuid4().hex)[:8]

    def run(self):
        self.tsLog = open(self.logName, 'w')

        for cnt in range(int(self.testSuite.getControl().getOpt(CONTROL_OPT_LOOP))):
            tsPId = self.genPId()
            self.testSuite.setPId(tsPId)
            self.tsSum.addTs(tsPId, self.testSuite.getId())
            self.runTs(tsPId)
            time.sleep(int(self.testSuite.getControl().getOpt(CONTROL_OPT_DELAY)))

        self.tsLog.write(str(self.tsSum))
        self.tsLog.close()
        self.tsShow.printSum(self.tsSum)

    def runTs(self, tsPId):
        for testCase in self.testSuite.getTestCases():
            for cnt in range(int(testCase.getControl().getOpt(CONTROL_OPT_LOOP))):
                tcPId = self.genPId()
                testCase.setPId(tcPId)
                self.tsSum.getTs(tsPId).addTc(tcPId, testCase.getId())
                self.runTc(tsPId, tcPId, testCase)

                self.tsLog.write(str(testCase))
                self.tsShow.printTc(testCase)
                testCase.clean()

                time.sleep(int(testCase.getControl().getOpt(CONTROL_OPT_DELAY)))

    def runTc(self, tsPId, tcPId, testCase):
        for restCase in testCase.getRestCases():
            rcPId = self.genPId()
            restCase.setPId(rcPId)

            restCase.setResponse(Response(self.runFunc(restCase.getRequest().getProperty())))
            restCase.getRequest().setStartTime(restCase.getResponse().getStartTime())

            self.tsSum.getTs(tsPId).getTc(tcPId).addRc(rcPId, restCase.getRcId(), \
                             restCase.getMethod(), restCase.getUrl(), restCase.checkResult())
            self.tsShow.printRc()
