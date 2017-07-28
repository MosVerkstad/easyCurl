#!/usr/bin/python

import sys

class Show:
    PROGRESS_BAR_LENGTH = 50

    DISPLAY_PROGRESS = 'progress'
    DISPLAY_VERBOSE  = 'verbose'

    def __init__(self, display, total):
        self.display = display
        self.total = total
        self.current = 0

    def verbose(self): return self.display == self.DISPLAY_VERBOSE
    def progress(self): return self.display == self.DISPLAY_PROGRESS

    def printProgress(self):
        progress = '%.2f%%' % (self.current * 1.0 / self.total * 100)
        barComplete = int(self.current * 1.0 / self.total * self.PROGRESS_BAR_LENGTH)
        barUncomplete = self.PROGRESS_BAR_LENGTH - barComplete
        barShow = '[' + '='*barComplete + ' '*barUncomplete + ']'
        barShow = barShow + progress + ' (' + str(self.current) + '/' + str(self.total) + ')'
        sys.stdout.write('\r' + barShow)
        sys.stdout.flush()

    def printRc(self):
        self.current += 1
        if self.progress(): self.printProgress()

    def printTc(self, tc):
        if self.verbose(): print tc

    def printSum(self, tsSum):
        print
        print tsSum
