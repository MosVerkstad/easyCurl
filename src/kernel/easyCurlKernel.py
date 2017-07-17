#!/usr/bin/python

import pycurl
from datetime import datetime
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from easyCurlConfig import optCurlMethods, optCurlLogName

def setOptCurl(c, opts):
    for opt in opts:
        if opt[1] == 'int':    c.setopt(eval(opt[0]), int(eval(opt[2])))
        elif opt[1] == 'bool': c.setopt(eval(opt[0]), bool(eval(opt[2])))
        elif opt[1] == 'str':  c.setopt(eval(opt[0]), str(eval(opt[2])))
        elif opt[1] == 'raw':  c.setopt(eval(opt[0]), opt[2])
    return c

def runCurl(requestObj):
    global url, method, requestHeaders, requestBodyStr
    url, method, requestHeaders, requestBodyStr = requestObj
    requestBody = BytesIO(requestBodyStr)
    responseHeaders = BytesIO()
    responseBody = BytesIO()
    responseCode, responseHeaderStr, responseBodyStr = None, None, None

    cType = method if optCurlMethods.get(method, None) != None else 'OTHERS'
    c = setOptCurl(setOptCurl(pycurl.Curl(), optCurlMethods['COMMON']), optCurlMethods[cType])

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
        responseCode, responseHeaderStr, responseBodyStr, startTime, endTime, error = None, None, None, None, None, e
    else:
        responseCode, responseHeaderStr, responseBodyStr, error = c.getinfo(pycurl.RESPONSE_CODE), responseHeaders.getvalue(), responseBody.getvalue(), None
    finally:
        c.close()
        requestBody.close()
        responseHeaders.close()
        responseBody.close()

    return responseCode, responseHeaderStr, responseBodyStr, startTime, endTime, error