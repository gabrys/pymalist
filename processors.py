import email
import email.utils

class NotAuthorized(Exception):
    pass

class NoSuchList(Exception):
    pass

class DummyProcessor(object):
    def process(self, mail):
        return mail

class SingleListProcessor(object):
    def __init__(self, list_email, subject_prefix, subscribers):
        self.list_email = list_email
        self.subject_prefix = subject_prefix
        self.subscribers = subscribers

    def process(self, mail):
        try:
            sender = mail['From']
        except:
            raise NotAuthorized, "empty From, rejecting"
        
        if email.utils.parseaddr(sender)[1] not in self.subscribers:
            raise NotAuthorized, sender
        
        try: del(mail['Reply-to'])
        except: pass
        mail['Reply-to'] = self.list_email

        try: del(mail['Sender'])
        except: pass
        mail['Sender'] = self.list_email

        try:
            subject = mail['Subject']
            del(mail['Subject'])
        except:
            subject = "(No subject)"

        if -1 == subject.find(self.subject_prefix):
            subject = self.subject_prefix + subject

        mail['Subject'] = subject
        mail.ml_sender = sender
        mail.ml_list = self.list_email
        mail.ml_send_to = self.subscribers

        return mail

class MoreListsProcessor(object):
    def __init__(self, *args):
        self.lists = {}
        for list in args:
            mail = email.utils.parseaddr(list.list_email)[1]
            self.lists[mail] = list

    def process(self, msg):
        try:
            to = email.utils.parseaddr(msg['To'])[1]
            list = self.lists[to]
        except:
            raise NoSuchList
        else:
            return list.process(msg)

