import email
import email.utils

class NotAuthorized(Exception):
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
        
        subject = msg['Subject']

        try: del(msg['Sender'])
        except: pass
        msg['Sender'] = self.list_mail

        try: del(msg['Reply-to'])
        except: pass
        msg['Reply-to'] = self.list_mail

        try: del(msg['Subject'])
        except: pass
        msg['Subject'] = self.subject_prefix + subject

        return 'list', sender, msg.as_string(), self.subscribers

