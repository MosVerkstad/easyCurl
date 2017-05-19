#!/usr/bin/python
URL    = 'http://easyCurl.com/test/objs'
URL_ID = 'http://easyCurl.com/test/objs/myObj'
METHOD_POST   = 'POST'
METHOD_GET    = 'GET'
METHOD_DELETE = 'DELETE'
HEADERS = ['Content-Type: application/json;charset=UTF-8', 'Accept: application/json']
BODY_POST  = '{"id":"myObj","description":" the obj created for testing purpose","version":"0.0.1","validity":true}'
BODY_EMPTY = ''

OBJ_POST   = (URL, METHOD_POST, HEADERS, BODY_POST)
OBJ_GET    = (URL, METHOD_GET, HEADERS, BODY_EMPTY)
OBJ_DELETE = (URL_ID, METHOD_DELETE, HEADERS, BODY_EMPTY)

testcaseList = [OBJ_GET, OBJ_POST, OBJ_GET, OBJ_DELETE, OBJ_GET]
