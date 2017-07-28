#!/usr/bin/env python

from constants import *

class SumRc:
    def __init__(self, rcPId, rcId, method, url, result):
        self.rcPId = rcPId
        self.rcId = rcId
        self.method = method
        self.url = url
        self.verdict, self.info = result
        self.indent = ' '*8

    def getVerdict(self):
        return self.verdict

    def __str__(self):
        infoStr = '' if self.verdict == KEYWORD_RESULT_PASS else self.info
        return self.indent + '(' + self.rcPId + ': ' + self.verdict + ') ' + \
               self.rcId + ' ' + infoStr + '\n'

class SumTc:
    def __init__(self, tcPId, tcId):
        self.tcPId = tcPId
        self.tcId = tcId
        self.rcList = list()
        self.rcDict = dict()
        self.tcVerdict = KEYWORD_RESULT_UNKNOWN
        self.indent = ' '*4

    def addRc(self, rcPId, rcId, method, url, result):
        rc = SumRc(rcPId, rcId, method, url, result)
        self.rcList.append(rc)
        self.rcDict[rcPId] = rc

    def getRc(self, rcPId):
        return self.rcDict[rcPId]

    def calcSum(self):
        u, p, f = 0, 0, 0
        vList = [rc.getVerdict() for rc in self.rcList]
        l = len(vList)
        for v in vList:
            if v == KEYWORD_RESULT_UNKNOWN: u = u + 1
            elif v == KEYWORD_RESULT_PASS: p = p + 1
            elif v == KEYWORD_RESULT_FAIL: f = f + 1
        if KEYWORD_RESULT_FAIL in vList: self.tcVerdict = KEYWORD_RESULT_FAIL
        elif KEYWORD_RESULT_PASS in vList: self.tcVerdict = KEYWORD_RESULT_PASS
        else: self.tcVerdict = KEYWORD_RESULT_UNKNOWN
        return u, p, f, l

    def getVerdict(self):
        return self.tcVerdict

    def getTcSum(self):
        u, p, f, l = self.calcSum()
        tcSum = self.indent + self.tcId + \
              ' (' + self.tcPId + ': ' + self.tcVerdict + ') ' + \
              KEYWORD_RESULT_PASS + ': ' + str(p) + '/' + str(l-u) + '; ' + \
              KEYWORD_RESULT_FAIL + ': ' + str(f) + '/' + str(l-u) + '; ' + \
              KEYWORD_RESULT_UNKNOWN + ': ' + str(u) + '\n'
        return tcSum

    def __str__(self):
        return self.getTcSum() + ''.join([str(rc) for rc in self.rcList])

class SumTs:
    def __init__(self, tsPId, tsId):
        self.tsPId = tsPId
        self.tsId = tsId
        self.tcList = list()
        self.tcDict = dict()

    def addTc(self, tcPId, tcId):
        tc = SumTc(tcPId, tcId)
        self.tcList.append(tc)
        self.tcDict[tcPId] = tc

    def getTc(self, tcPId):
        return self.tcDict[tcPId]

    def getTsSum(self):
        tsSum = ''.join([str(tc) for tc in self.tcList])
        u, p, f = 0, 0, 0
        vList = [tc.getVerdict() for tc in self.tcList]
        l = len(vList)
        for v in vList:
            if v == KEYWORD_RESULT_UNKNOWN: u = u + 1
            elif v == KEYWORD_RESULT_PASS: p = p + 1
            elif v == KEYWORD_RESULT_FAIL: f = f + 1
        tsSum = self.tsId + ' (' + self.tsPId + ') ' + \
              KEYWORD_RESULT_PASS + ': ' + str(p) + '/' + str(l-u) + '; ' + \
              KEYWORD_RESULT_FAIL + ': ' + str(f) + '/' + str(l-u) + '; ' + \
              KEYWORD_RESULT_UNKNOWN + ': ' + str(u) + '\n' + \
              tsSum
        return tsSum

    def __str__(self):
         return self.getTsSum()

class Sum:
    def __init__(self):
        self.tsList = list()
        self.tsDict = dict()

    def addTs(self, tsPId, tsId):
        ts = SumTs(tsPId, tsId)
        self.tsList.append(ts)
        self.tsDict[tsPId] = ts

    def getTs(self, tsPId):
        return self.tsDict[tsPId]

    def __str__(self):
        return ''.join([str(ts) for ts in self.tsList])
