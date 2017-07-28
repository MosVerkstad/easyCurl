#!/usr/bin/env python

from constants import *

class Request:
    def __init__(self, obj):
        self.rcId, self.url, self.method, self.headers, self.body = \
        None,      None,     None,        None,         None
        self.startTime = None
        self.setProperty(obj)

    def setProperty(self, obj):
        if isinstance(obj, dict):
            self.rcId, self.url, self.method, self.headers, self.body = \
            obj[KEYWORD_RCID], obj[KEYWORD_URL], obj[KEYWORD_METHOD], obj[KEYWORD_HEADERS], obj[KEYWORD_BODY]
        elif isinstance(obj, tuple):
            self.rcId, self.url, self.method, self.headers, self.body = obj

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getProperty(self):
        return self.rcId, self.url, self.method, self.headers, self.body

    def getBody(self):
        return self.body

    def getMethod(self):
        return self.method

    def __str__(self):
        strStartTime = '(' + str(self.startTime) + ')' if self.startTime != None else ''
        return 'REST CASE REQUEST ID: ' + self.rcId + '\n' + \
               '>>>> REST REQUEST SEND: ' + strStartTime + '\n' + self.method + ' ' + \
               self.url + '\n' + \
               ', '.join(self.headers) + '\n' + self.body + '\n'

class Response:
    def __init__(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime, self.error = obj

    def setProperty(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime, self.error = obj

    def getProperty(self):
        return self.statusCode, self.headers, self.body, self.startTime, self.endTime, self.error

    def getStatusCode(self):
        return self.statusCode

    def getError(self):
        return self.error

    def getDuration(self):
        return self.endTime - self.startTime if self.endTime != None and self.startTime != None else 0

    def getStartTime(self):
        return self.startTime

    def __str__(self):
        strEndTime = '(' + str(self.endTime) + ')' if self.endTime != None else ''
        return '<<<< REST RESPONSE RECEIVE: ' + strEndTime + '\n    (LATENCY: ' + \
               str(self.getDuration()) + ')\n' + \
               str(self.headers) + '\n' + str(self.body) + '\n'

class Control:
    def getDefaultOpts(self):
        return {'LOOP': '1', 'DELAY': '0'}

    def __init__(self, controlLine=''):
        self.optControls = self.getDefaultOpts()
        if controlLine != '':
            for c in controlLine.split(','):
                pair = c.split(':')
                if len(pair) == 2: key, value = pair[0].strip(), pair[1].strip()
                else: key, value = None, None
                if key != None and self.optControls.get(key, None) != None:
                    self.optControls[key] = value

    def getOpt(self, key):
        return self.optControls[key]

class Expect:
    def __init__(self, obj):
        self.optExpect = {}
        expectLine = obj.get(KEYWORD_EXPECT, '')
        if expectLine != '':
            for e in expectLine.split(','):
                pair = e.split(':')
                if len(pair) == 2: key, value = pair[0].strip(), pair[1].strip()
                else: key, value = None, None
                if key != None:
                    if key == 'STATUSCODE': self.optExpect[key] = value.split('|')
                    else: self.optExpect[key] = value

    def checkStatusCode(self, statusCode):
        result = (KEYWORD_RESULT_UNKNOWN, 'EXPECT is not set.')
        if self.optExpect.get('STATUSCODE', None) != None:
            detail = 'EXPECT: ' + str(self.optExpect['STATUSCODE']) + '; RESULT: ' + str(statusCode)
            result = (KEYWORD_RESULT_PASS, detail) \
                     if str(statusCode) in self.optExpect['STATUSCODE'] else (KEYWORD_RESULT_FAIL, detail)
        return result

class RestCase:
    def __init__(self, request, expect):
        self.request = request
        self.expect = expect
        self.response = None
        self.pId = None

    def setRequest(self, request):
        self.request = request

    def getRequest(self):
        return self.request

    def setResponse(self, response):
        self.response = response

    def getResponse(self):
        return self.response

    def setPId(self, pId):
        self.pId = pId

    def getPId(self):
        return self.pId

    def getRcId(self):
        i, u, m, h, b = self.request.getProperty()
        return i

    def getMethod(self):
        i, u, m, h, b = self.request.getProperty()
        return m

    def getUrl(self):
        i, u, m, h, b = self.request.getProperty()
        return u

    def checkResult(self):
        if self.response != None:
            if self.response.getStatusCode() != None:
                return self.expect.checkStatusCode(self.response.getStatusCode())
            else:
                return (KEYWORD_RESULT_FAIL, str(self.response.getError()))
        else:
            return (KEYWORD_RESULT_FAIL, 'NO RESPONSE')

    def __str__(self):
        return 'REST CASE PROCESS ID: ' + str(self.pId) + '\n' + \
               str(self.request) + str(self.response) + '\n' + \
               str(self.checkResult()) + '\n' + '='*80 + '\n\n'

class TestCase:
    def __init__(self, tcId, tcObj):
        self.tcId = tcId
        self.tcRestCases = [RestCase(Request(rc),Expect(rc)) for rc in tcObj[KEYWORD_RC]] \
                           if tcObj.get(KEYWORD_RC, None) != None else None
        self.tcControl = Control(tcObj[KEYWORD_CONTROL]) \
                         if tcObj.get(KEYWORD_CONTROL, None) != None else Control()
        self.pId = None

    def getId(self):
        return self.tcId

    def getRestCases(self):
        return self.tcRestCases

    def getControl(self):
        return self.tcControl

    def setPId(self, pId):
        self.pId = pId

    def clean(self):
        for rc in self.tcRestCases:
            rc.setResponse(None)
            rc.setPId(None)

    def __str__(self):
        return 'TEST CASE: ' + self.tcId + ' ' + \
               '( PROCESS ID: ' + str(self.pId) + ')\n' + \
               ''.join([str(rc) for rc in self.tcRestCases])

class TestSuite:
    def __init__(self, tsId, tsObj):
        self.tsId = tsId
        self.tsTestCases = [TestCase(tc.keys()[0], tc.values()[0]) for tc in tsObj[KEYWORD_TC]] \
                           if tsObj.get(KEYWORD_TC, None) != None else None
        self.tsControl = Control(tsObj[KEYWORD_CONTROL]) \
                         if tsObj.get(KEYWORD_CONTROL, None) != None else Control()
        self.pId = None

    def getId(self):
        return self.tsId

    def getTestCases(self):
        return self.tsTestCases

    def getControl(self):
        return self.tsControl

    def setPId(self, pId):
        self.pId = pId
