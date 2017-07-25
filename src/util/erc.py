#!/usr/bin/env python

from vdy import vdy

class erc:
    RC_TEMPLATE = 'RC_TEMPLATE'

    def __init__(self, vdyObj, ercDoc):
        self.vdyObj = vdyObj
        self.ercDoc = ercDoc

    def rc(self, rcName):
        rcItem = self.ercDoc[rcName]
        copy = vdy()
        return copy.clone(self.vdyObj).join(rcItem).assign()[self.RC_TEMPLATE]