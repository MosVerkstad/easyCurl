#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.cfg import getErcConfig, getArgv

def generateTs(args):
    context = '../common/CONTEXTS_OM.vdy'
    erc = 'RC_OM_BASIC.erc'
    fileNames = args + ',' + context + ',' + erc
    KEYWORD_TC = 'TESTCASES'
    KEYWORD_RC = 'RESTCASES'

    print fileNames
    e = getErcConfig(getArgv(fileNames))

    return {'TS_PM_BASIC': \
               {KEYWORD_TC: \
                   [ \
                   {'TC_BASIC_BULK': {KEYWORD_RC:[\
                        e.rc('RC_GROUPS_GET_WRONGURL'), \
                        e.rc('RC_GROUPS_GET_WRONGBODY'), \
                        e.rc('RC_GROUPS_GET'), \
                        e.rc('RC_GROUPS_POST'), \
                        e.rc('RC_GROUPS_GET'), \
                        e.rc('RC_GROUPS_DELETE'), \
                        e.rc('RC_GROUPS_GET'), \
                   ]}},\
                   ]
               }
           }
