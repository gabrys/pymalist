import base64
import smtplib
import email

class UnknownType(Exception):
    pass

class DistributeToDistributor(object):
    def __init__(self, recipients, distributor):
        self.recipients = recipients
        self.distributor = distributor

    def distribute(self, mail):
        mail.ml_send_to = self.recipients
        self.distributor.distribute(mail)

class SmtpDistributor(object):
    def __init__(self, host='localhost', user=None, password='', ssl=False, tls=False, sender=None):
        if ssl:
            self.smtp = smtplib.SMTP_SSL(host)
        else:
            self.smtp = smtplib.SMTP(host)
        if tls:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()
        if user:
            try:
                self.smtp.login(user, password)
            except smtplib.SMTPAuthenticationError, e:
                self.smtp.docmd("AUTH LOGIN", base64.b64encode(user))
                self.smtp.docmd(base64.b64encode(password), "")
                
        self.sender = sender
    
    def distribute(self, mail):
        if self.sender:
            sender = self.sender
        else:
            sender = mail.ml_sender
        for recipient in mail.ml_send_to:
            self.smtp.sendmail(sender, recipient, mail.as_string())
    
    def __del__(self):
        self.smtp.quit()

class MultipleDistributor(object):
    def __init__(self, *args):
        self.distributors = args

    def distribute(self, mail):
        for distributor in self.distributors:
            distributor.distribute(mail)

def UniversalDistributor(options):
    type = options['distributor']
    del(options['distributor'])
    if type.upper() == 'SMTP':
        return SmtpDistributor(**options)
    else:
        raise UnknownType, "%s distributor is unknown" % (type, )
