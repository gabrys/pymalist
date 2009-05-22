import email
import email.utils

class NotAuthorized(Exception):
    pass

class NoSuchList(Exception):
    pass

class DummyProcessor(object):
    def process(self, msg):
        return '', '', msg, []

class SingleListProcessor():
    def __init__(self, list_mail, subject_prefix, subscribers):
        self.list_mail = list_mail
        self.subject_prefix = subject_prefix
        self.subscribers = subscribers

    def process(self, msg):
        msg = email.message_from_string(msg)
        try:
            sender = msg['From']
        except:
            raise NotAuthorized, "empty From, rejecting"
        
        if email.utils.parseaddr(sender)[1] not in self.subscribers:
            raise NotAuthorized, sender
        
        try: del(msg['Sender'])
        except: pass
        msg['Sender'] = self.list_mail

        try: del(msg['Reply-to'])
        except: pass
        msg['Reply-to'] = self.list_mail

        try:
            subject = msg['Subject']
            del(msg['Subject'])
        except:
            subject = "(No subject)"

        if not subject.find(subject_prefix):
            subject = subject_prefix + subject

        msg['Subject'] = subject

        return 'list', sender, msg.as_string(), self.subscribers

class MoreListsProcessor():
    def __init__(self, *args):
        self.lists = {}
        for list in args:
            mail = email.utils.parseaddr(list.list_mail)[1]
            self.lists[mail] = list

    def process(self, msg_str):
        try:
            msg = email.message_from_string(msg_str)
            to = email.utils.parseaddr(msg['To'])[1]
            list = self.lists[to]
        except:
            raise NoSuchList
        else:
            return list.process(msg_str)

