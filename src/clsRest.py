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
        return 'clsRestRequ: (' + self.url + '; ' + self.method + '; ' + \
               ','.join(self.headers) + '; ' + self.body + ')'

class Response:
    def __int__(self):
        self.statusCode = None
        self.headers = None
        self.body = None

    def __init__(self, statusCode, headers, body):
        self.statusCode = statusCode
        self.headers = headers
        self.body = body

    def __init__(self, obj):
        self.statusCode, self.headers, self.body = obj

    def setProperty(self, obj):
        self.statusCode, self.headers, self.body = obj

    def getProperty(self):
        return self.statusCode, self.headers, self.body

    def __str__(self):
        return 'clsRestResp: (' + str(self.statusCode) + '; ' + \
               self.headers + '; ' + self.body + ')'


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