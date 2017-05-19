#!/usr/bin/python

# URL for FOR ALL CASES
URL       = 'http://easyCurl.com/test/objs'
URL_OBJ01 = 'http://easyCurl.com/test/objs/myObj01'
URL_OBJ02 = 'http://easyCurl.com/test/objs/myObj02'

# REST METHOD FOR ALL OF CASES
METHOD_POST   = 'POST'
METHOD_GET    = 'GET'
METHOD_DELETE = 'DELETE'
METHOD_PUT    = 'PUT'

# REQUEST HEADERS FOR ALL OF CASES
HEADERS = ['Content-Type: application/json;charset=UTF-8', 'Accept: application/json']

# REQUEST BODY FOR ALL OF CASES
BODY_POST_OBJ01  = '{"id":"myObj","description":" the obj created for testing purpose","version":"0.0.1","validity":true}'
BODY_PUT_OBJ02   = '{"description":" the second obj created for testing purpose","version":"0.0.1","validity":true}'
BODY_EMPTY       = ''

OBJ_POST_OBJ01   = (URL, METHOD_POST, HEADERS, BODY_POST_OBJ01)
OBJ_PUT_OBJ02    = (URL_OBJ02, METHOD_PUT, HEADERS, BODY_PUT_OBJ02)
OBJ_GET          = (URL, METHOD_GET, HEADERS, BODY_EMPTY)
OBJ_DELETE_OBJ01 = (URL_OBJ01, METHOD_DELETE, HEADERS, BODY_EMPTY)
OBJ_DELETE_OBJ02 = (URL_OBJ02, METHOD_DELETE, HEADERS, BODY_EMPTY)

# THE TEST CASE LIST WHICH SHOULD BE RUN IN EASYCURL
testcaseList = [OBJ_GET,
                OBJ_POST_OBJ01,
                OBJ_PUT_OBJ02,
                OBJ_GET,
                OBJ_DELETE_OBJ01,
                OBJ_DELETE_OBJ02,
                OBJ_GET]
