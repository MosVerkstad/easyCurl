#!/usr/bin/env python

class Request:
    def __init_(self):
        self.url = None
        self.method = None
        self.headers = None
        self.body = None

    def __init__(self, url, method, headers, body):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def __init__(self, obj):
        self.url, self.method, self.headers, self.body = obj

    def setProperty(self, obj):
        self.url, self.method, self.headers, self.body = obj

    def getProperty(self):
        return self.url, self.method, self.headers, self.body

    def getBody(self):
        return self.body

    def __str__(self):
        return '>>>> REST REQUEST SEND: \n\t' + self.url + '\n\t' + \
               self.method + '\n\t' + \
               ', '.join(self.headers) + '\n\t' + self.body + '\n'

class Response:
    def __int__(self):
        self.statusCode = None
        self.headers = None
        self.body = None
        self.startTime = None
        self.endTime = None

    def __init__(self, statusCode, headers, body, startTime, endTime):
        self.statusCode = statusCode
        self.headers = headers
        self.body = body
        self.startTime = startTime
        self.endTime = endTime

    def __init__(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime = obj

    def setProperty(self, obj):
        self.statusCode, self.headers, self.body, self.startTime, self.endTime = obj

    def getProperty(self):
        return self.statusCode, self.headers, self.body, self.startTime, self.endTime

    def getDuration(self):
        return self.endTime - self.startTime

    def __str__(self):
        return '<<<< REST RESPONSE RECEIVE: \n==== LATENCY: ' + \
               str(self.getDuration()) + ' ====\n' + str(self.statusCode) + \
               '\n' + self.headers + '\n' + self.body + '\n'

class RestCase:
    def __init__(self):
        self.request = None
        self.response = None

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
    def __init__(self, tcId, tcRestCaseList):
        self.tcId = tcId
        self.tcRestCases = [RestCase(Request(rc)) for rc in tcRestCaseList]

    def getId(self):
        return self.tcId

    def getRestCases(self):
        return self.tcRestCases

    def __str__(self):
        return 'TEST CASE: ' + self.tcId + '\n' + ''.join([str(rc) for rc in self.tcRestCases])

class TestSuite:
    def __init__(self, tsId, tsTestCaseList):
        self.tsId = tsId
        self.tsTestCases = [TestCase(tcId, tcRestCaseList) for (tcId, tcRestCaseList) in tsTestCaseList]

    def getId(self):
        return self.tsId

    def getTestCases(self):
        return self.tsTestCases