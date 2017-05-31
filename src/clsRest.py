#!/usr/bin/env python

KEYWORD_URL = 'URL'
KEYWORD_METHOD = 'METHOD'
KEYWORD_HEADERS = 'HEADERS'
KEYWORD_BODY = 'BODY'
KEYWORD_CONTROL = 'CONTROL'
KEYWORD_EXPECT = 'EXPECT'
KEYWORD_RC = 'RESTCASES'
KEYWORD_TC = 'TESTCASES'

class Request:
    def __init__(self, obj):
        if isinstance(obj, dict):
            self.url, self.method, self.headers, self.body = \
            obj[KEYWORD_URL], obj[KEYWORD_METHOD], obj[KEYWORD_HEADERS], obj[KEYWORD_BODY]
            self.startTime = None
        elif isinstance(obj, tuple):
            self.url, self.method, self.headers, self.body = obj
            self.startTime = None

    def setProperty(self, obj):
        if isinstance(obj, dict):
            self.url, self.method, self.headers, self.body = \
            obj[KEYWORD_URL], obj[KEYWORD_METHOD], obj[KEYWORD_HEADERS], obj[KEYWORD_BODY]
        elif isinstance(obj, tuple):
            self.url, self.method, self.headers, self.body = obj

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getProperty(self):
        return self.url, self.method, self.headers, self.body

    def getBody(self):
        return self.body

    def __str__(self):
        strStartTime = '(' + str(self.startTime) + ')' if self.startTime != None else ''
        return '>>>> REST REQUEST SEND: ' + strStartTime + '\n\t' + self.url + '\n\t' + \
               self.method + '\n\t' + \
               ', '.join(self.headers) + '\n\t' + self.body + '\n'

class Response:
    def __init__(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime = obj

    def setProperty(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime = obj

    def getProperty(self):
        return self.statusCode, self.headers, self.body, self.startTime, self.endTime

    def getDuration(self):
        return self.endTime - self.startTime

    def getStartTime(self):
        return self.startTime

    def __str__(self):
        strEndTime = '(' + str(self.endTime) + ')' if self.endTime != None else ''
        return '<<<< REST RESPONSE RECEIVE: ' + strEndTime + '\n==== LATENCY: ' + \
               str(self.getDuration()) + ' ====\n' + str(self.statusCode) + \
               '\n' + self.headers + '\n' + self.body + '\n'

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

class RestCase:
    def __init__(self, request):
        self.request = request
        self.response = None

    def setRequest(self, request):
        self.request = request

    def getRequest(self):
        return self.request

    def setResponse(self, response):
        self.response = response

    def getResponse(self):
        return self.response

    def __str__(self):
        return str(self.request) + str(self.response) + '\n'

class TestCase:
    def __init__(self, tcId, tcObj):
        self.tcId = tcId
        self.tcRestCases = [RestCase(Request(rc)) for rc in tcObj[KEYWORD_RC]] \
                           if tcObj.get(KEYWORD_RC, None) != None else None
        self.tcControl = Control(tcObj[KEYWORD_CONTROL]) \
                         if tcObj.get(KEYWORD_CONTROL, None) != None else Control()

    def getId(self):
        return self.tcId

    def getRestCases(self):
        return self.tcRestCases

    def getControl(self):
        return self.tcControl

    def __str__(self):
        return 'TEST CASE: ' + self.tcId + '\n' + ''.join([str(rc) for rc in self.tcRestCases])

class TestSuite:
    def __init__(self, tsId, tsObj):
        self.tsId = tsId
        self.tsTestCases = [TestCase(tc.keys()[0], tc.values()[0]) for tc in tsObj[KEYWORD_TC]] \
                           if tsObj.get(KEYWORD_TC, None) != None else None
        self.tsControl = Control(tsObj[KEYWORD_CONTROL]) \
                         if tsObj.get(KEYWORD_CONTROL, None) != None else Control()

    def getId(self):
        return self.tsId

    def getTestCases(self):
        return self.tsTestCases

    def getControl(self):
        return self.tsControl