#!/usr/bin/python

import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from easyCurlConfig import optCurlMethods

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
        c.perform()
    except Exception as e:
        responseCode, responseHeaderStr, responseBodyStr = None, None, None
    else:
        responseCode, responseHeaderStr, responseBodyStr = c.getinfo(pycurl.RESPONSE_CODE), responseHeaders.getvalue(), responseBody.getvalue()
    finally:
        c.close()
        requestBody.close()
        responseHeaders.close()
        responseBody.close()

    return responseCode, responseHeaderStr, responseBodyStr

from easyCurlTest import restCaseList
from clsRest import *

if(__name__ == '__main__'):
    for restCase in restCaseList:
        requestBodyStr = restCase.getRequest().getBody() 
        restCase.setResponse(Response(runCurl(restCase.getRequest().getProperty())))
        print restCase.getResponse()