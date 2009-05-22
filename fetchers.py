
import sys

class NothingMore(Exception):
    pass

class StdInFetcher(object):
    def __init__(self):
        self.read = False

    def fetch(self):
        if self.read:
            raise NothingMore
        else:
            val = sys.stdin.read()
            self.read = True
            return val

