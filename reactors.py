
import sys

class StdErrLogger(object):
    def react(self, type, e):
        sys.stderr.write("%s: %s\n" % (type, str(e)))

