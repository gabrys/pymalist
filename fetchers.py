
import sys
import poplib

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

class Pop3Fetcher(object):
    def __init__(self, host, user, password, ssl=False):
        if ssl:
            self.pop = poplib.POP3_SSL(host)
        else:
            self.pop = poplib.POP3(host)
        self.pop.user(user)
        self.pop.pass_(password)
        self.mails = [line.split(" ")[0] for line in self.pop.list()[1]]
    
    def fetch(self):
        try:
            mailno = self.mails.pop(0)
        except IndexError:
            raise NothingMore
        mail = self.pop.retr(mailno)[1]
        self.pop.dele(mailno)
        return "\n".join(mail)

    def __del__(self):
        self.pop.quit()

