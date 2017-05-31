#!/usr/bin/python

# REST METHOD SUPPORTED BY EASYCURL, OF COURSE YOU CAN ADD MORE
optCurlMethods = {'COMMON': [('pycurl.TIMEOUT', 'int', '10'),
                             ('pycurl.VERBOSE', 'bool', 'False')],
                  'GET'   : [('pycurl.HTTPGET', 'int', '1')],
                  'POST'  : [('pycurl.POST', 'int', '1'),
                             ('pycurl.POSTFIELDSIZE', 'int', 'len(requestBodyStr)')],
                  'PUT'   : [('pycurl.UPLOAD', 'int', '1'),
                             ('pycurl.INFILESIZE', 'int', 'len(requestBodyStr)')],
                  'DELETE': [('pycurl.CUSTOMREQUEST', 'raw', 'DELETE')]
}

# LOG FILE NAME
optCurlLogName = 'EASYCURL_DAILY.log'