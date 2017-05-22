#!/usr/bin/python

optCurlMethods = {'COMMON': [('pycurl.TIMEOUT', 'int', '10'),
                             ('pycurl.VERBOSE', 'bool', 'False')],
                  'GET'   : [('pycurl.HTTPGET', 'int', '1')],
                  'POST'  : [('pycurl.POST', 'int', '1'),
                             ('pycurl.POSTFIELDSIZE', 'int', 'len(requestBodyStr)')],
                  'PUT'   : [('pycurl.UPLOAD', 'int', '1'),
                             ('pycurl.INFILESIZE', 'int', 'len(requestBodyStr)')],
                  'DELETE': [('pycurl.CUSTOMREQUEST', 'raw', 'DELETE')]
}