
import smtplib
import email

class DistributeToDistributor(object):
    def __init__(self, recipient, distributor):
        self.recipient = recipient
        self.distributor = distributor

    def distribute(self, list, sender, message, recipients):
        self.distributor.distribute(list, sender, self.recipient, message)

class SmtpDistributor(object):
    def __init__(self, host='localhost', user=None, password='', ssl=False, tls=False):
        if ssl:
            self.smtp = smtplib.SMTP_SSL(host)
        else:
            self.smtp = smtplib.SMTP(host)
        if tls:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()
        if user:
            self.smtp.login(user, password)
    
    def distribute(self, list, sender, message, recipients):
        mail = email.message_from_string(message)
        for recipient in recipients:
            self.smtp.sendmail(sender, recipient, mail.as_string())
    
    def __del__(self):
        self.smtp.quit()

class ChainDistributor(object):
    def __init__(self, *args):
        self.distributors = args

    def distribute(self, list, sender, message, recipients):
        for distributor in self.distributors:
            distributor.distribute(list, sender, message, recipients)

