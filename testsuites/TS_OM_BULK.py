#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.cfg import getErcConfig, getArgv

def generateTs(args):
    context = '../common/CONTEXTS_OM.vdy'
    erc = 'RC_OM_BASIC.erc,RC_OM_BULK.erc'
    fileNames = args + ',' + context + ',' + erc
    KEYWORD_TC = 'TESTCASES'
    KEYWORD_RC = 'RESTCASES'

    e = getErcConfig(getArgv(fileNames))

    return {'TS_OM_BASIC': \
               {KEYWORD_TC: \
                   [ \
                   {'TC_BULK_OM': {KEYWORD_RC:[\
                        e.rc('RC_GROUPS_GET'), \
                        e.rc('RC_BULK_GROUPS_METRICS_CREATE'), \
                        e.rc('RC_GROUPS_GET'), \
                        e.rc('RC_BULK_GROUPS_METRICS_DELETE'), \
                        e.rc('RC_GROUPS_GET'), \
                   ]}},\
                   ]
               }
           }
